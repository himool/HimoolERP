from utils.permissions import IsAuthenticated, PurchasePricePermission
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import CategorySerializer, GoodsSerializer
from .permissions import CategoryPermission, GoodsPermission
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from warehouse.models import Inventory, Flow
from purchase.models import ChangeRecord
from .paginations import GoodsPagination
from rest_framework import viewsets
from django.db import transaction
from utils import math


class CategoryViewSet(viewsets.ModelViewSet):
    """商品分类: list, post, update, delete"""
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, CategoryPermission]
    filter_backends = [OrderingFilter]
    ordering_fields = ['order']
    ordering = ['order']

    def get_queryset(self):
        return self.request.user.teams.category_set.all()

    def perform_create(self, serializer):
        serializer.save(teams=self.request.user.teams)


class GoodsViewSet(viewsets.ModelViewSet):
    """商品:　list, post, update, delete"""
    serializer_class = GoodsSerializer
    permission_classes = [IsAuthenticated, GoodsPermission, PurchasePricePermission]
    pagination_class = GoodsPagination
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filter_fields = ['name', 'category', 'status']
    search_fields = ['name', 'code']
    ordering_fields = ['name', 'code', 'purchase_price', 'suggested_retail_price', 'retail_price', 'order']
    ordering = ['order']

    def get_queryset(self):
        return self.request.user.teams.goods_set.filter(is_delete=False)

    @transaction.atomic
    def perform_create(self, serializer):
        code = self.request.data.get('code')
        teams = self.request.user.teams

        # 商品货号已存在
        if teams.goods_set.filter(is_delete=False, code=code).first():
            raise ValidationError({'message': '商品货号已存在'})
        serializer.save(teams=teams)

        # 创建库存
        goods = serializer.instance
        goods_form = self.request.data
        inventory_set = []
        flows = []
        initial_quantity = 0
        for warehouse in teams.warehouse_set.filter(is_delete=False, status=True):
            quantity = goods_form['inventory'].get(str(warehouse.id), 0)
            inventory_set.append(Inventory(goods=goods, warehouse=warehouse, quantity=quantity, teams=teams))
            if quantity != 0:
                initial_quantity = math.plus(initial_quantity, quantity)
                flows.append(Flow(goods=goods, goods_code=goods.code, goods_name=goods.name, type='初始化库存',
                                  specification=goods.specification, unit=goods.unit, warehouse=warehouse,
                                  warehouse_name=warehouse.name, change_quantity=quantity,
                                  remain_quantity=quantity, operator=self.request.user, teams=teams))

        goods.initial_quantity = initial_quantity
        goods.save()
        Inventory.objects.bulk_create(inventory_set)
        Flow.objects.bulk_create(flows)

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        teams = request.user.teams

        # 商品货号禁止修改
        if request.data.get('code') != instance.code:
            raise ValidationError

        # 采购价变更记录
        purchase_price = request.data.get('purchase_price', 0)
        if purchase_price != instance.purchase_price:
            goods = serializer.instance
            ChangeRecord.objects.create(goods=goods, goods_code=goods.code, goods_name=goods.name, teams=teams,
                                        specification=goods.specification, unit=goods.unit, change_method='手动',
                                        before_change=instance.purchase_price, after_change=goods.purchase_price,
                                        operator=request.user)

        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        return Response(serializer.data)

    @transaction.atomic
    def perform_destroy(self, instance):
        instance.is_delete = True
        instance.save()

        # 删除所有库存
        instance.inventory_set.all().delete()
