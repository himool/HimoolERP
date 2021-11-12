from extensions.permissions import *
from extensions.exceptions import *
from extensions.viewsets import *
from apps.sales.serializers import *
from apps.sales.permissions import *
from apps.sales.filters import *
from apps.sales.schemas import *
from apps.sales.models import *
from apps.goods.models import *
from apps.flow.models import *
from apps.stock_out.models import *


class SalesOrderViewSet(BaseViewSet, ListModelMixin, RetrieveModelMixin, CreateModelMixin):
    """销售单据"""

    serializer_class = SalesOrderSerializer
    permission_classes = [IsAuthenticated, SalesOrderPermission]
    filterset_class = SalesOrderFilter
    search_fields = ['number', 'client__number', 'client__name', 'remark']
    ordering_fields = ['id', 'number', 'total_quantity', 'total_amount', 'create_time']
    select_related_fields = ['warehouse', 'client', 'handler', 'creator']
    prefetch_related_fields = ['sales_goods_set', 'sales_goods_set__goods',
                               'sales_goods_set__goods__unit',
                               'collection_order__collection_accounts',
                               'collection_order__collection_accounts__account']
    queryset = SalesOrder.objects.all()

    @transaction.atomic
    def perform_create(self, serializer):
        sales_order = serializer.save()

        # 同步出库
        if sales_order.enable_auto_stock_out:
            # 同步库存, 流水
            inventory_flows = []
            for sales_goods in sales_order.sales_goods_set.all():
                inventory = Inventory.objects.get(warehouse=sales_order.warehouse,
                                                  goods=sales_goods.goods, team=self.team)
                quantity_before = inventory.total_quantity
                quantity_change = sales_goods.sales_quantity
                quantity_after = NP.minus(quantity_before, quantity_change)

                inventory_flows.append(InventoryFlow(
                    warehouse=sales_order.warehouse, goods=sales_goods.goods,
                    type=InventoryFlow.Type.SALES, quantity_before=quantity_before,
                    quantity_change=quantity_change, quantity_after=quantity_after,
                    sales_order=sales_order, creator=self.user, team=self.team
                ))

                inventory.total_quantity = quantity_after
                inventory.save(update_fields=['total_quantity'])
            else:
                InventoryFlow.objects.bulk_create(inventory_flows)
        else:
            # 创建出库单据
            stock_out_order_number = StockOutOrder.get_number(team=self.team)
            stock_out_order = StockOutOrder.objects.create(
                number=stock_out_order_number, warehouse=sales_order.warehouse,
                type=StockOutOrder.Type.SALES, sales_order=sales_order,
                total_quantity=sales_order.total_quantity,
                remain_quantity=sales_order.total_quantity,
                creator=self.user, team=self.team
            )

            # 创建出库商品
            stock_out_goods_set = []
            for sales_goods in sales_order.sales_goods_set.all():
                stock_out_goods_set.append(StockOutGoods(
                    stock_out_order=stock_out_order, goods=sales_goods.goods,
                    stock_out_quantity=sales_goods.sales_quantity, team=self.team
                ))
            else:
                StockOutGoods.objects.bulk_create(stock_out_goods_set)

        # 同步欠款
        client = sales_order.client
        client.arrears_amount = NP.plus(client.arrears_amount, client.arrears_amount)
        client.save(update_fields=['arrears_amount'])

        # 同步账户, 流水
        if collection_order := sales_order.collection_order:
            finance_flows = []
            for collection_account in collection_order.collection_accounts.all():
                account = collection_account.account
                amount_before = account.balance_amount
                amount_change = collection_account.collection_amount
                amount_after = NP.plus(amount_before, amount_change)

                finance_flows.append(FinanceFlow(
                    account=account, type=FinanceFlow.Type.COLLECTION, amount_before=amount_before,
                    amount_change=amount_change, amount_after=amount_after,
                    collection_order=collection_order, creator=self.user, team=self.team
                ))

                account.balance_amount = amount_after
                account.save(update_fields=['balance_amount'])
            else:
                FinanceFlow.objects.bulk_create(finance_flows)

    @extend_schema(responses={200: NumberResponse})
    @action(detail=False, methods=['get'])
    def number(self, request, *args, **kwargs):
        """获取编号"""

        number = SalesOrder.get_number(self.team)
        return Response(data={'number': number}, status=status.HTTP_200_OK)

    @transaction.atomic
    @extend_schema(request=None, responses={200: SalesOrderSerializer})
    @action(detail=True, methods=['post'])
    def void(self, request, *args, **kwargs):
        """作废"""

        sales_order = self.get_object()
        if sales_order.is_void:
            raise ValidationError(f'销售单据[{sales_order.number}]已作废, 无法再次作废')

        # 同步销售单据, 销售商品
        sales_order.is_void = True
        sales_order.save(update_fields=['is_void'])
        sales_order.sales_goods_set.all().update(is_void=True)

        # 同步出库
        if sales_order.enable_auto_stock_out:
            # 同步库存, 流水
            inventory_flows = []
            for sales_goods in sales_order.sales_goods_set.all():
                inventory = Inventory.objects.get(warehouse=sales_order.warehouse,
                                                  goods=sales_goods.goods, team=self.team)
                quantity_before = inventory.total_quantity
                quantity_change = sales_goods.sales_quantity
                quantity_after = NP.plus(quantity_before, quantity_change)

                inventory_flows.append(InventoryFlow(
                    warehouse=sales_order.warehouse, goods=sales_goods.goods,
                    type=InventoryFlow.Type.VOID_SALES, quantity_before=quantity_before,
                    quantity_change=quantity_change, quantity_after=quantity_after,
                    void_sales_order=sales_order, creator=self.user, team=self.team
                ))

                inventory.total_quantity = quantity_after
                inventory.save(update_fields=['total_quantity'])
            else:
                InventoryFlow.objects.bulk_create(inventory_flows)
        else:
            # 作废出库单据
            stock_out_order = sales_order.stock_out_order
            if stock_out_order.total_quantity != stock_out_order.remain_quantity:
                raise ValidationError(f'销售单据[{sales_order.number}]无法作废, 已存在出库记录')

            stock_out_order.is_void = True
            stock_out_order.save(update_fields=['is_void'])

            # 作废出库商品
            stock_out_order.stock_out_goods_set.all().update(is_void=True)

        # 同步欠款
        client = sales_order.client
        client.arrears_amount = NP.minus(client.arrears_amount, sales_order.arrears_amount)
        client.save(update_fields=['arrears_amount'])

        # 同步账户, 流水
        if collection_order := sales_order.collection_order:
            # 作废收款单据
            collection_order.is_void = True
            collection_order.save(update_fields=['is_void'])

            # 作废收款账号
            collection_order.collection_accounts.all().update(is_void=True)

            finance_flows = []
            for collection_account in collection_order.collection_accounts.all():
                account = collection_account.account
                amount_before = account.balance_amount
                amount_change = collection_account.collection_amount
                amount_after = NP.minus(amount_before, amount_change)

                finance_flows.append(FinanceFlow(
                    account=account, type=FinanceFlow.Type.VOID_PAYMENT, amount_before=amount_before,
                    amount_change=amount_change, amount_after=amount_after,
                    void_collection_order=collection_order, creator=self.user, team=self.team
                ))

                account.balance_amount = amount_after
                account.save(update_fields=['balance_amount'])
            else:
                FinanceFlow.objects.bulk_create(finance_flows)

        serializer = SalesOrderSerializer(instance=sales_order)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


__all__ = [
    'SalesOrderViewSet',
]
