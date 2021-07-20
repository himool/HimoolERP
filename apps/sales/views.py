from .serializers import SalesOrderSerializer, SalesTaskSerializer, ClientSerializer, SalesOrderProfitSerializer, SalesPaymentRecordSerializer
from .paginations import SalesOrderPagination, SalesTaskPagination, ClientPagination, SalesOrderProfitPagination, SalesPaymentRecordPagination
from utils.permissions import IsAuthenticated, PurchasePricePermission
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .filters import SalesTaskFilter, SalesOrderProfitFilter, SalesPaymentRecordFilter, SalesOrderFilter
from .models import SalesGoods, SalesOrder, PaymentRecord
from warehouse.models import Inventory, Warehouse, Flow
from rest_framework.status import HTTP_201_CREATED
from rest_framework.exceptions import APIException
from .permissions import SalesOrderPermission
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, status
from datetime import datetime, timedelta
from django.db.models import F, Sum
from account.models import Account
from django.db import transaction
from sales.models import Client
from goods.models import Goods
from user.models import User
from utils import math
import pendulum


class SalesOrderViewSet(viewsets.ModelViewSet):
    """list, create, destroy"""
    serializer_class = SalesOrderSerializer
    permission_classes = [IsAuthenticated, SalesOrderPermission]
    pagination_class = SalesOrderPagination
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filterset_class = SalesOrderFilter
    search_fields = ['id', 'client_name', 'client_phone', 'remark']
    ordering_fields = ['id', 'date', 'total_amount', 'amount']
    ordering = ['-id']

    def get_queryset(self):
        return self.request.user.teams.sales_order_set.all()

    @transaction.atomic
    def perform_create(self, serializer):
        order_id = f'S{pendulum.now().format("YYYYMMDDHHmmssSSSS")}'
        teams = self.request.user.teams

        # 验证
        if self.request.data.get('is_return', False):  # 退货单
            sales_order = self.request.data.get('sales_order')
            sales_order = SalesOrder.objects.filter(
                id=sales_order, is_done=True, is_return=False, teams=teams).first()
            if not sales_order:
                raise ValidationError
            warehouse = sales_order.warehouse
        else:
            warehouse = self.request.data.get('warehouse')
            warehouse = Warehouse.objects.filter(id=warehouse, teams=teams, is_delete=False).first()

        seller = self.request.data.get('seller')
        if seller == self.request.user.username:
            seller = self.request.user
        else:
            seller = User.objects.filter(id=seller, teams=teams, is_delete=False).first()

        account = self.request.data.get('account')
        account = Account.objects.filter(id=account, teams=teams, is_delete=False).first()

        if not warehouse or not account or not seller:
            raise ValidationError

        # 创建客户
        client = None
        client_phone = self.request.data.get('client_phone')
        if client_phone:
            client = Client.objects.filter(teams=teams, phone=client_phone).first()
            if not client:
                client_name = self.request.data.get('client_name')
                client_contacts = self.request.data.get('client_contacts')
                client_address = self.request.data.get('client_address')
                Client.objects.create(phone=client_phone, name=client_name, contacts=client_contacts,
                                      address=client_address, teams=teams)
            elif client.is_delete:
                client.is_delete = False
                client.save()

        # 创建表单商品
        goods_set = self.request.data.get('goods_set', [])
        goods_id_set = map(lambda item: item['id'], goods_set)
        goods_list = Goods.objects.filter(id__in=goods_id_set, is_delete=False, teams=teams)

        if len(goods_set) != len(goods_list):
            raise ValidationError

        discount = self.request.data.get('discount', 100)
        total_quantity = 0
        total_amount = 0
        sales_goods_set = []
        for goods1 in goods_list:
            for goods2 in goods_set:
                if goods1.id == goods2['id']:
                    amount = math.times(goods2['quantity'], goods2['retail_price'], discount, 0.01)
                    total_quantity = math.plus(total_quantity, goods2['quantity'])
                    total_amount = math.plus(total_amount, amount)

                    sales_goods_set.append(
                        SalesGoods(goods=goods1, code=goods1.code, name=goods1.name, unit=goods1.unit,
                                   specification=goods1.specification, quantity=goods2['quantity'],
                                   purchase_price=goods1.purchase_price, retail_price=goods2['retail_price'],
                                   amount=amount, remark=goods2.get('remark'), sales_order_id=order_id))
                    break

        serializer.save(teams=teams, id=order_id, warehouse_name=warehouse.name,
                        account_name=account.name, total_quantity=total_quantity, total_amount=total_amount,
                        client=client)
        SalesGoods.objects.bulk_create(sales_goods_set)

        # 创建付款记录
        amount = self.request.data.get('amount', 0)
        if amount != 0:
            PaymentRecord.objects.create(amount=amount, account=account, account_name=account.name,
                                         sales_order=serializer.instance)

    @action(detail=False)
    @transaction.atomic
    def confirm(self, request, *args, **kwargs):
        teams = request.user.teams
        order_id = request.data.get('id')
        if not order_id:
            raise ValidationError

        sales_order = SalesOrder.objects.filter(teams=teams, is_done=False, id=order_id).first()
        if not sales_order:
            raise ValidationError

        # 同步仓库, 创建流水
        flows = []
        for sales_goods in sales_order.goods_set.all().iterator():
            inventory = Inventory.objects.filter(
                teams=teams, goods=sales_goods.goods, warehouse=sales_order.warehouse).first()
            if not inventory:
                raise APIException({'message': '表单已失效 (仓库/门店 或 商品 已被删除)'})
            change_quantity = sales_goods.quantity if sales_order.is_return else -sales_goods.quantity
            inventory.quantity = math.plus(inventory.quantity, change_quantity)
            inventory.save()

            type = '销售退货单' if sales_order.is_return else '销售单'
            flows.append(Flow(type=type, teams=teams, goods=sales_goods.goods, goods_code=sales_goods.code,
                              goods_name=sales_goods.name, specification=sales_goods.specification,
                              unit=sales_goods.unit, warehouse=sales_order.warehouse,
                              warehouse_name=sales_order.warehouse_name, change_quantity=change_quantity,
                              remain_quantity=inventory.quantity, operator=request.user, sales_order=sales_order))

        Flow.objects.bulk_create(flows)

        sales_order.is_done = True
        sales_order.save()
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

        order = SalesOrder.objects.filter(teams=teams, id=order_id).first()
        account = Account.objects.filter(teams=teams, id=account, is_delete=False).first()
        if not order or not account:
            raise ValidationError
        if order.amount + amount > order.total_amount:
            raise ValidationError({'message': '金额已超出'})

        PaymentRecord.objects.create(amount=amount, account=account, account_name=account.name,
                                     sales_order=order, remark=remark)
        order.amount = math.plus(order.amount, amount)
        order.save()
        return Response({'id': order.id, 'amount': order.amount}, status=HTTP_201_CREATED)


class SalesPaymentRecordViewSet(viewsets.ModelViewSet):
    """销售支付记录: list"""
    serializer_class = SalesPaymentRecordSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = SalesPaymentRecordPagination
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    filterset_class = SalesPaymentRecordFilter
    ordering_fields = ['sales_order', 'date', 'amount']
    ordering = ['-date']

    def get_queryset(self):
        return PaymentRecord.objects.filter(sales_order__teams=self.request.user.teams)


class SalesTaskViewSet(viewsets.ModelViewSet):
    """销售任务: list, create"""
    serializer_class = SalesTaskSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = SalesTaskPagination
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    filterset_class = SalesTaskFilter
    ordering_fields = ['create_date']
    ordering = ['-create_date']

    def get_queryset(self):
        return self.request.user.teams.sales_tasks.all()

    def perform_create(self, serializer):
        end_date = self.request.data['end_date']
        end_date = pendulum.parse(end_date).add(days=1)
        serializer.save(end_date=end_date, teams=self.request.user.teams)


class SalesOrderProfitViewSet(viewsets.ModelViewSet):
    """利润统计: list, update (修改成本)"""
    serializer_class = SalesOrderProfitSerializer
    permission_classes = [IsAuthenticated, PurchasePricePermission]
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    pagination_class = SalesOrderProfitPagination
    filterset_class = SalesOrderProfitFilter
    search_fields = ['id']
    ordering_fields = ['id', 'date']
    ordering = ['-id']

    def get_queryset(self):
        return self.request.user.teams.sales_order_set.filter(is_return=False)

    def update(self, request, *args, **kwargs):
        sales_goods_id = kwargs.get('pk')
        purchase_price = request.data.get('purchase_price')
        if not sales_goods_id or not purchase_price:
            raise ValidationError

        SalesGoods.objects.filter(
            sales_order__teams=request.user.teams, id=sales_goods_id).update(purchase_price=purchase_price)
        return Response(status=status.HTTP_200_OK)

    @action(detail=False)
    def total_profit(self, request, *args, **kwargs):
        warehouse = request.GET.get('warehouse')
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        queryset = SalesGoods.objects.filter(sales_order__teams=request.user.teams, sales_order__is_return=False)
        if warehouse:
            queryset = queryset.filter(sales_order__warehouse_id=warehouse)
        if start_date:
            queryset = queryset.filter(sales_order__date__gte=start_date)
        if end_date:
            end_date = pendulum.parse(end_date).add(days=1)
            queryset = queryset.filter(sales_order__date__lte=end_date)

        total_profit = queryset.aggregate(total_profit=Sum(
            (F('retail_price') * F('sales_order__discount') * 0.01 - F('purchase_price')) * F('quantity'))).get('total_profit')
        return Response({'total_profit': total_profit if total_profit else 0})


class SalesValueViewSet(viewsets.ViewSet):
    """销售额"""
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')

        if not start_date or not end_date:
            raise ValidationError
        end_date = pendulum.parse(end_date).add(days=1)

        queryset = SalesOrder.objects.filter(teams=request.user.teams, is_return=False)
        queryset = queryset.filter(date__gte=start_date, date__lte=end_date)
        queryset = queryset.extra(select={'_date': 'DATE_FORMAT(date, "%%Y-%%m-%%d")'})
        queryset = queryset.values('_date', _warehouse=F('warehouse__name'))
        results = queryset.annotate(_amount=Sum('total_amount'))

        warehouse_list = Warehouse.objects.filter(
            teams=request.user.teams, is_delete=False).values_list('name', flat=True)
        return Response({'results': results, 'warehouse_list': warehouse_list})


class SalesTopTenViewSet(viewsets.ViewSet):
    """销售前十"""
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')

        if not start_date or not end_date:
            raise ValidationError
        end_date = pendulum.parse(end_date).add(days=1)

        queryset = SalesGoods.objects.filter(sales_order__teams=request.user.teams, sales_order__is_return=False)
        queryset = queryset.filter(sales_order__date__gte=start_date, sales_order__date__lte=end_date)
        queryset = queryset.values(_goods=F('goods__name'))
        results = queryset.annotate(_quantity=Sum('quantity')).order_by('-_quantity')[:10]

        return Response({'results': results})


class ClientViewSet(viewsets.ModelViewSet):
    """list, create, destroy"""
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = ClientPagination
    filter_backends = [SearchFilter]
    search_fields = ['phone', 'name']

    def get_queryset(self):
        return self.request.user.teams.clients.filter(is_delete=False).order_by('-create_date')

    def perform_create(self, serializer):
        teams = self.request.user.teams
        phone = self.request.data['phone']
        client = Client.objects.filter(phone=phone, teams=teams).first()
        if not client:
            serializer.save(teams=teams)
        elif client.is_delete:
            client.is_delete = False
            client.save()
        else:
            raise ValidationError({'message': '客户已存在'})

    def perform_destroy(self, instance):
        instance.is_delete = True
        instance.save()
