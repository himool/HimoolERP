from .permissions import WarehousePermission, InventoryPermission, FlowPermission, CountingListPermission, RequisitionPermission
from .serializers import WarehouseSerializer, FlowSerializer, CountingListSerializer, RequisitionSerializer, InventorySerializer
from .paginations import FlowPagination, CountingListPagination, RequisitionPagination, InventoryPagination
from utils.permissions import IsAuthenticated, PurchasePricePermission
from rest_framework.exceptions import APIException, ValidationError
from .models import CountingListGoods, RequisitionGoods, Warehouse
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import F, Sum, Q, Count, Value
from .filters import FlowFilter, InventoryFilter
from rest_framework.decorators import api_view
from rest_framework.response import Response
from warehouse.models import Inventory, Flow
from rest_framework.decorators import action
from django.db import models, transaction
from django.http import HttpResponse
from rest_framework import viewsets
from goods.models import Goods
from utils import math
import pendulum
import csv


class WarehouseViewSet(viewsets.ModelViewSet):
    """list, create, update, destroy"""
    serializer_class = WarehouseSerializer
    permission_classes = [IsAuthenticated, WarehousePermission]
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    filter_fields = ['status']
    ordering_fields = ['name', 'manager', 'create_date', 'order']
    ordering = ['order']

    def get_queryset(self):
        return self.request.user.teams.warehouse_set.filter(is_delete=False)

    @transaction.atomic
    def perform_create(self, serializer):
        teams = self.request.user.teams
        serializer.save(teams=teams)

        goods_set = teams.goods_set.filter(is_delete=False)
        Inventory.objects.bulk_create([Inventory(goods=goods, warehouse=serializer.instance, teams=teams)
                                       for goods in goods_set])

    @transaction.atomic
    def perform_destroy(self, instance):
        instance.is_delete = True
        instance.save()

        # 删除所有库存
        instance.inventory_set.all().delete()


class InventoryViewSet(viewsets.ModelViewSet):
    """list"""
    serializer_class = InventorySerializer
    permission_classes = [IsAuthenticated, InventoryPermission, PurchasePricePermission]
    filter_backends = [DjangoFilterBackend]
    filterset_class = InventoryFilter
    pagination_class = InventoryPagination

    def get_queryset(self):
        return self.request.user.teams.inventory_set.all()

    @action(detail=False)
    def export(self, request, *args, **kwargs):
        queryset = InventoryFilter(request.GET)
        if not queryset.is_valid():
            raise ValidationError

        queryset = queryset.filter_queryset(request.user.teams.inventory_set.all())
        results = queryset.all().values('quantity', code=F('goods__code'), name=F('goods__name'), brand=F('goods__brand'),
                                        category_name=F('goods__category__name'), specification=F('goods__specification'),
                                        unit=F('goods__unit'), purchase_price=F('goods__purchase_price'),
                                        warehouse_name=F('warehouse__name'))

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment;filename=inventory.csv'

        writer = csv.DictWriter(response, ['code', 'name', 'brand', 'specification', 'unit', 'category_name',
                                           'warehouse_name', 'quantity', 'purchase_price'])
        writer.writeheader()
        writer.writerows(results)
        return response


class FlowViewSet(viewsets.ModelViewSet):
    """list"""
    serializer_class = FlowSerializer
    permission_classes = [IsAuthenticated, FlowPermission]
    pagination_class = FlowPagination
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filterset_class = FlowFilter
    search_fields = ['goods_code', 'goods_name']
    ordering_fields = ['create_datetime', 'goods_code', 'goods_name', 'change_quantity', 'remain_quantity']
    ordering = ['-create_datetime']

    def get_queryset(self):
        return self.request.user.teams.flows.all()


class CountingListViewSet(viewsets.ModelViewSet):
    """list, create, retrieve"""
    serializer_class = CountingListSerializer
    permission_classes = [IsAuthenticated, CountingListPermission, PurchasePricePermission]
    pagination_class = CountingListPagination
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filter_fields = ['warehouse']
    search_fields = ['id', 'remark']
    ordering_fields = ['id', 'date']
    ordering = ['-id']

    def get_queryset(self):
        return self.request.user.teams.counting_list_set.all()

    @transaction.atomic
    def perform_create(self, serializer):
        order_id = f'C{pendulum.now().format("YYYYMMDDHHmmssSSSS")}'
        teams = self.request.user.teams

        # 验证
        warehouse = self.request.data.get('warehouse')
        warehouse = Warehouse.objects.filter(id=warehouse, teams=teams, is_delete=False).first()
        if not warehouse:
            raise ValidationError

        # 创建表单商品, 同步仓库, 创建流水
        goods_set = self.request.data.get('goods_set', [])
        goods_id_set = map(lambda item: item['id'], goods_set)
        goods_list = Goods.objects.filter(id__in=goods_id_set, is_delete=False, teams=teams)

        if len(goods_set) != len(goods_list):
            raise ValidationError

        flows = []
        counting_goods_set = []
        total_quantity = 0
        profit_quantity = 0
        profit_amount = 0
        for goods1 in goods_list:
            for goods2 in goods_set:
                if goods1.id == goods2['id']:
                    inventory = Inventory.objects.filter(teams=teams, goods=goods1, warehouse=warehouse).first()
                    if not inventory:
                        raise APIException

                    change_quantity = goods2['quantity'] - inventory.quantity
                    total_quantity = math.plus(total_quantity, goods2['quantity'])
                    profit_quantity = math.plus(profit_quantity, change_quantity)
                    profit_amount = math.plus(profit_amount, math.times(change_quantity, goods1.purchase_price))

                    counting_goods_set.append(CountingListGoods(goods=goods1, code=goods1.code, name=goods1.name,
                                                                unit=goods1.unit, specification=goods1.specification,
                                                                quantity=goods2['quantity'], before_counting=inventory.quantity,
                                                                purchase_price=goods1.purchase_price, counting_list_id=order_id))

                    flows.append(Flow(type='盘点单', teams=teams, goods=goods1, goods_code=goods1.code,
                                      goods_name=goods1.name, specification=goods1.specification,
                                      unit=goods1.unit, warehouse=warehouse, warehouse_name=warehouse.name,
                                      change_quantity=change_quantity, remain_quantity=goods2['quantity'],
                                      operator=self.request.user, counting_list_id=order_id))

                    inventory.quantity = goods2['quantity']
                    inventory.save()
                    break

        serializer.save(id=order_id, warehouse_name=warehouse.name, total_quantity=total_quantity,
                        profit_quantity=profit_quantity, profit_amount=profit_amount, teams=teams)
        CountingListGoods.objects.bulk_create(counting_goods_set)
        Flow.objects.bulk_create(flows)


class RequisitionViewSet(viewsets.ModelViewSet):
    """list, create, update, destroy"""
    serializer_class = RequisitionSerializer
    permission_classes = [IsAuthenticated, RequisitionPermission]
    pagination_class = RequisitionPagination
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filter_fields = ['out_warehouse', 'into_warehouse']
    search_fields = ['id', 'remark']
    ordering_fields = ['id', 'date']
    ordering = ['-id', 'date']

    def get_queryset(self):
        return self.request.user.teams.requisition_set.all()

    @transaction.atomic
    def perform_create(self, serializer):
        order_id = f'R{pendulum.now().format("YYYYMMDDHHmmssSSSS")}'
        teams = self.request.user.teams

        # 验证
        out_warehouse = self.request.data.get('out_warehouse')
        out_warehouse = Warehouse.objects.filter(id=out_warehouse, teams=teams, is_delete=False).first()
        into_warehouse = self.request.data.get('into_warehouse')
        into_warehouse = Warehouse.objects.filter(id=into_warehouse, teams=teams, is_delete=False).first()
        if not out_warehouse or not into_warehouse:
            raise ValidationError

        # 创建表单商品, 同步仓库, 创建流水
        goods_set = self.request.data.get('goods_set', [])
        goods_id_set = map(lambda item: item['id'], goods_set)
        goods_list = Goods.objects.filter(id__in=goods_id_set, is_delete=False, teams=teams)

        if len(goods_set) != len(goods_list):
            raise ValidationError

        flows = []
        requisition_goods_set = []
        total_quantity = 0
        for goods1 in goods_list:
            for goods2 in goods_set:
                if goods1.id == goods2['id']:
                    out_inventory = Inventory.objects.filter(teams=teams, goods=goods1, warehouse=out_warehouse).first()
                    into_inventory = Inventory.objects.filter(teams=teams, goods=goods1, warehouse=into_warehouse).first()

                    if not out_inventory or not into_inventory:
                        raise APIException

                    change_quantity = goods2['quantity']
                    out_inventory.quantity = math.minus(out_inventory.quantity, change_quantity)
                    into_inventory.quantity = math.plus(into_inventory.quantity, change_quantity)
                    out_inventory.save()
                    into_inventory.save()
                    total_quantity = math.plus(total_quantity, goods2['quantity'])

                    requisition_goods_set.append(RequisitionGoods(goods=goods1, code=goods1.code, name=goods1.name,
                                                                  unit=goods1.unit, specification=goods1.specification,
                                                                  quantity=goods2['quantity'],
                                                                  requisition_id=order_id))

                    flows.append(Flow(type='调拨单', teams=teams, goods=goods1, goods_code=goods1.code,
                                      goods_name=goods1.name, specification=goods1.specification,
                                      unit=goods1.unit, warehouse=out_warehouse, warehouse_name=out_warehouse.name,
                                      change_quantity=-change_quantity, remain_quantity=out_inventory.quantity,
                                      operator=self.request.user, requisition_id=order_id))
                    flows.append(Flow(type='调拨单', teams=teams, goods=goods1, goods_code=goods1.code,
                                      goods_name=goods1.name, specification=goods1.specification,
                                      unit=goods1.unit, warehouse=into_warehouse, warehouse_name=into_warehouse.name,
                                      change_quantity=change_quantity, remain_quantity=into_inventory.quantity,
                                      operator=self.request.user, requisition_id=order_id))
                    break

        serializer.save(id=order_id, out_warehouse_name=out_warehouse.name, total_quantity=total_quantity,
                        into_warehouse_name=into_warehouse.name, teams=teams)

        RequisitionGoods.objects.bulk_create(requisition_goods_set)
        Flow.objects.bulk_create(flows)
