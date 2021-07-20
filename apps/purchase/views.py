from .serializers import SupplierSerializer, PurchaseOrderSerializer, ChangeRecordSerializer, PurchasePaymentRecordSerializer
from .models import PurchaseOrder, PurchaseGoods, PaymentRecord, ChangeRecord, Supplier
from .paginations import PurchaseOrderPagination, ChangeRecordPagination, PurchasePaymentRecordPagination
from utils.permissions import IsAuthenticated, PurchasePricePermission
from .permissions import SupplierPermission, PurchaseOrderPermission
from rest_framework.exceptions import APIException, ValidationError
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.status import HTTP_201_CREATED
from warehouse.models import Inventory, Flow
from rest_framework.decorators import action
from rest_framework.response import Response
from warehouse.models import Warehouse
from django.db.models import Sum, F
from rest_framework import viewsets
from account.models import Account
from django.db import transaction
from goods.models import Goods
from user.models import User
from utils import math
import pendulum
from .filters import PurchasePaymentRecordFilter, PurchaseOrderFilter


class SupplierViewSet(viewsets.ModelViewSet):
    """list, create, update, destroy"""
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated, SupplierPermission]

    def get_queryset(self):
        return self.request.user.teams.supplier_set.filter(is_delete=False).order_by('order')

    def perform_create(self, serializer):
        serializer.save(teams=self.request.user.teams)

    def perform_destroy(self, instance):
        instance.is_delete = True
        instance.save()


class PurchaseOrderViewSet(viewsets.ModelViewSet):
    """list, create, update, destroy"""
    serializer_class = PurchaseOrderSerializer
    permission_classes = [IsAuthenticated, PurchaseOrderPermission, PurchasePricePermission]
    pagination_class = PurchaseOrderPagination
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filterset_class = PurchaseOrderFilter
    search_fields = ['id', 'supplier_name', 'warehouse_name']
    ordering_fields = ['id', 'date', 'total_amount', 'amount']
    ordering = ['-id']

    def get_queryset(self):
        return self.request.user.teams.purchase_order_set.all()

    @transaction.atomic
    def perform_create(self, serializer):
        order_id = f'P{pendulum.now().format("YYYYMMDDHHmmssSSSS")}'
        teams = self.request.user.teams
        print(1)
        # 验证
        if self.request.data.get('is_return', False):  # 退货单
            purchase_order = self.request.data.get('purchase_order')
            purchase_order = PurchaseOrder.objects.filter(
                id=purchase_order, is_done=True, is_return=False, teams=teams).first()
            if not purchase_order:
                raise ValidationError
            supplier = purchase_order.supplier
            warehouse = purchase_order.warehouse
        else:
            supplier = self.request.data.get('supplier')
            supplier = Supplier.objects.filter(id=supplier, teams=teams, is_delete=False).first()
            warehouse = self.request.data.get('warehouse')
            warehouse = Warehouse.objects.filter(id=warehouse, teams=teams, is_delete=False).first()
        print(2)

        account = self.request.data.get('account')
        account = Account.objects.filter(id=account, teams=teams, is_delete=False).first()
        contacts = self.request.data.get('contacts')
        contacts = User.objects.filter(id=contacts, teams=teams, is_delete=False).first()

        if not supplier or not warehouse or not account or not contacts:
            raise ValidationError
        print(3)

        # 创建表单商品
        goods_set = self.request.data.get('goods_set', [])
        goods_id_set = map(lambda item: item['id'], goods_set)
        goods_list = Goods.objects.filter(id__in=goods_id_set, is_delete=False, teams=teams)

        if len(goods_set) != len(goods_list):
            raise ValidationError
        print(4)

        change_records = []
        total_quantity = 0
        total_amount = 0
        purchase_goods_set = []
        for goods1 in goods_list:
            for goods2 in goods_set:
                if goods1.id == goods2['id']:
                    amount = math.times(goods2['quantity'], goods2['purchase_price'])
                    discount_amount = math.times(amount, goods2['discount'], 0.01)
                    discount_price = math.times(goods2['purchase_price'], goods2['discount'], 0.01)
                    total_quantity = math.plus(total_quantity, goods2['quantity'])
                    total_amount = math.plus(total_amount, discount_amount)

                    purchase_goods_set.append(PurchaseGoods(goods=goods1, code=goods1.code, name=goods1.name,
                                                            specification=goods1.specification, unit=goods1.unit,
                                                            quantity=goods2['quantity'], purchase_price=goods2['purchase_price'],
                                                            discount=goods2['discount'], discount_price=discount_price,
                                                            amount=amount, discount_amount=discount_amount,
                                                            purchase_order_id=order_id))

                    # 采购价变更
                    if goods1.purchase_price != goods2['purchase_price']:
                        change_records.append(ChangeRecord(
                            goods=goods1, goods_code=goods1.id, goods_name=goods1.name,
                            specification=goods1.specification, unit=goods1.unit, change_method='采购变价',
                            before_change=goods1.purchase_price, operator=self.request.user, teams=teams,
                            after_change=goods2['purchase_price'], relation_order=serializer.instance))

                        goods1.purchase_price = goods2['purchase_price']
                        goods1.save()
                    break
        print(5)

        serializer.save(id=order_id, supplier_name=supplier.name, warehouse_name=warehouse.name,
                        warehouse_address=warehouse.address, account_name=account.name,
                        contacts_phone=contacts.phone,
                        total_quantity=total_quantity, total_amount=total_amount, teams=teams)

        PurchaseGoods.objects.bulk_create(purchase_goods_set)

        # 创建付款记录
        amount = self.request.data.get('amount', 0)
        if amount != 0:
            PaymentRecord.objects.create(amount=amount, account=account, account_name=account.name,
                                         purchase_order=serializer.instance)

        ChangeRecord.objects.bulk_create(change_records)

    def perform_destroy(self, instance):
        if instance.is_done:
            raise APIException
        instance.delete()

    @action(detail=False)
    @transaction.atomic
    def confirm(self, request, *args, **kwargs):
        teams = request.user.teams
        order_id = request.data.get('id')
        if not order_id:
            raise ValidationError

        purchase_order = PurchaseOrder.objects.filter(teams=teams, is_done=False, id=order_id).first()
        if not purchase_order:
            raise ValidationError

        # 同步仓库, 创建流水
        flows = []
        for purchase_goods in purchase_order.goods_set.all().iterator():
            inventory = Inventory.objects.filter(
                teams=teams, goods=purchase_goods.goods, warehouse=purchase_order.warehouse).first()
            if not inventory:
                raise APIException({'message': '表单已失效 (仓库/门店 或 商品 已被删除)'})
            change_quantity = -purchase_goods.quantity if purchase_order.is_return else purchase_goods.quantity
            inventory.quantity = math.plus(inventory.quantity, change_quantity)
            inventory.save()

            type = '采购退货单' if purchase_order.is_return else '采购单'
            flows.append(Flow(type=type, teams=teams, goods=purchase_goods.goods, goods_code=purchase_goods.code,
                              goods_name=purchase_goods.name, specification=purchase_goods.specification,
                              unit=purchase_goods.unit, warehouse=purchase_order.warehouse,
                              warehouse_name=purchase_order.warehouse_name, change_quantity=change_quantity,
                              remain_quantity=inventory.quantity, operator=request.user, purchase_order=purchase_order))

        Flow.objects.bulk_create(flows)

        purchase_order.is_done = True
        purchase_order.save()
        return Response(status=HTTP_201_CREATED)

    @action(detail=False)
    @transaction.atomic
    def payment(self, request, *args, **kwargs):
        teams = request.user.teams
        order_id = request.data.get('id')
        amount = request.data.get('amount')
        account = request.data.get('account')
        remark = request.data.get('remark')

        # 验证
        if not order_id or not account or amount is None:
            raise ValidationError
        if amount <= 0:
            raise ValidationError({'message': '金额错误'})

        order = PurchaseOrder.objects.filter(teams=teams, id=order_id).first()
        account = Account.objects.filter(teams=teams, id=account, is_delete=False).first()
        if not order or not account:
            raise ValidationError
        if order.amount + amount > order.total_amount:
            raise ValidationError({'message': '金额已超出'})

        PaymentRecord.objects.create(amount=amount, account=account, account_name=account.name,
                                     purchase_order=order, remark=remark)
        order.amount = math.plus(order.amount, amount)
        order.save()
        return Response({'id': order.id, 'amount': order.amount}, status=HTTP_201_CREATED)


class PurchasePaymentRecordViewSet(viewsets.ModelViewSet):
    """采购支付记录: list"""
    serializer_class = PurchasePaymentRecordSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PurchasePaymentRecordPagination
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    filterset_class = PurchasePaymentRecordFilter
    ordering_fields = ['purchase_order', 'date', 'amount']
    ordering = ['-date']

    def get_queryset(self):
        return PaymentRecord.objects.filter(purchase_order__teams=self.request.user.teams)


class ChangeRecordViewSet(viewsets.ModelViewSet):
    """采购价变更记录: list"""
    serializer_class = ChangeRecordSerializer
    permission_classes = [IsAuthenticated, PurchasePricePermission]
    pagination_class = ChangeRecordPagination
    filter_backends = [OrderingFilter]
    ordering_fields = ['create_datetime', 'goods_code', 'goods_name', 'change_method', 'before_change',
                       'after_change', 'operator']
    ordering = ['-create_datetime']

    def get_queryset(self):
        return self.request.user.teams.change_records.all()
