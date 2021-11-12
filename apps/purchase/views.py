from extensions.permissions import *
from extensions.exceptions import *
from extensions.viewsets import *
from apps.purchase.serializers import *
from apps.purchase.permissions import *
from apps.purchase.filters import *
from apps.purchase.schemas import *
from apps.purchase.models import *
from apps.goods.models import *
from apps.flow.models import *
from apps.stock_in.models import *


class PurchaseOrderViewSet(BaseViewSet, ListModelMixin, RetrieveModelMixin, CreateModelMixin):
    """采购单据"""

    serializer_class = PurchaseOrderSerializer
    permission_classes = [IsAuthenticated, PurchaseOrderPermission]
    filterset_class = PurchaseOrderFilter
    search_fields = ['number', 'supplier__number', 'supplier__name', 'remark']
    ordering_fields = ['id', 'number', 'total_quantity', 'total_amount', 'create_time']
    select_related_fields = ['warehouse', 'supplier', 'handler', 'creator']
    prefetch_related_fields = ['purchase_goods_set', 'purchase_goods_set__goods__unit',
                               'payment_order__payment_accounts']
    queryset = PurchaseOrder.objects.all()

    @transaction.atomic
    def perform_create(self, serializer):
        purchase_order = serializer.save()

        # 同步入库
        if purchase_order.enable_auto_stock_in:
            # 同步库存, 流水
            inventory_flows = []
            for purchase_goods in purchase_order.purchase_goods_set.all():
                inventory = Inventory.objects.get(warehouse=purchase_order.warehouse,
                                                  goods=purchase_goods.goods, team=self.team)
                quantity_before = inventory.total_quantity
                quantity_change = purchase_goods.purchase_quantity
                quantity_after = NP.plus(inventory.total_quantity, purchase_goods.purchase_quantity)

                inventory_flows.append(InventoryFlow(
                    warehouse=purchase_order.warehouse, goods=purchase_goods.goods,
                    type=InventoryFlow.Type.PURCHASE, quantity_before=quantity_before,
                    quantity_change=quantity_change, quantity_after=quantity_after,
                    purchase_order=purchase_order, creator=self.user, team=self.team
                ))

                inventory.total_quantity = quantity_after
                inventory.save(update_fields=['total_quantity'])
            else:
                InventoryFlow.objects.bulk_create(inventory_flows)
        else:
            # 创建入库单据
            stock_in_order_number = StockInOrder.get_number(team=self.team)
            stock_in_order = StockInOrder.objects.create(
                number=stock_in_order_number, warehouse=purchase_order.warehouse,
                type=StockInOrder.Type.PURCHASE, purchase_order=purchase_order,
                total_quantity=purchase_order.total_quantity, creator=self.user, team=self.team
            )

            # 创建入库商品
            stock_in_goods_set = []
            for purchase_goods in purchase_order.purchase_goods_set.all():
                stock_in_goods_set.append(StockInGoods(
                    stock_in_order=stock_in_order, goods=purchase_goods.goods,
                    stock_in_quantity=purchase_goods.purchase_quantity, team=self.team
                ))
            else:
                StockInGoods.objects.bulk_create(stock_in_goods_set)

        # 同步欠款
        supplier = purchase_order.supplier
        supplier.arrears_amount = NP.plus(supplier.arrears_amount, purchase_order.arrears_amount)
        supplier.save(update_fields=['arrears_amount'])

        # 同步账户, 流水
        if payment_order := purchase_order.payment_order:
            finance_flows = []
            for payment_account in payment_order.payment_accounts.all():
                account = payment_account.account
                amount_before = account.balance_amount
                amount_change = payment_account.payment_amount
                amount_after = NP.minus(amount_before, amount_change)

                finance_flows.append(FinanceFlow(
                    account=payment_account.account, type=FinanceFlow.Type.PAYMENT,
                    amount_before=amount_before, amount_change=amount_change, amount_after=amount_after,
                    payment_order=payment_order, creator=self.user, team=self.team
                ))

                account.balance_amount = amount_after
                account.save(update_fields=['balance_amount'])
            else:
                FinanceFlow.objects.bulk_create(finance_flows)

    @extend_schema(responses={200: NumberResponse})
    @action(detail=False, methods=['get'])
    def number(self, request, *args, **kwargs):
        """获取编号"""

        number = PurchaseOrder.get_number(self.team)
        return Response(data={'number': number}, status=status.HTTP_200_OK)

    @transaction.atomic
    @extend_schema(request=None, responses={200: PurchaseOrderSerializer})
    @action(detail=True, methods=['post'])
    def void(self, request, *args, **kwargs):
        """作废"""

        purchase_order = self.get_object()
        if purchase_order.is_void:
            raise ValidationError(f'采购单据[{purchase_order.number}]已作废, 无法再次作废')

        # 同步采购单据, 采购商品
        purchase_order.is_void = True
        purchase_order.save(update_fields=['is_void'])
        purchase_order.purchase_goods_set.all().update(is_void=True)

        # 同步入库
        if purchase_order.enable_auto_stock_in:
            # 同步库存, 流水
            inventory_flows = []
            for purchase_goods in purchase_order.purchase_goods_set.all():
                inventory = Inventory.objects.get(warehouse=purchase_order.warehouse,
                                                  goods=purchase_goods.goods, team=self.team)
                quantity_before = inventory.total_quantity
                quantity_change = purchase_goods.purchase_quantity
                quantity_after = NP.minus(inventory.total_quantity, purchase_goods.purchase_quantity)

                inventory_flows.append(InventoryFlow(
                    warehouse=purchase_order.warehouse, goods=purchase_goods.goods,
                    type=InventoryFlow.Type.VOID_PURCHASE, quantity_before=quantity_before,
                    quantity_change=quantity_change, quantity_after=quantity_after,
                    void_purchase_order=purchase_order, creator=self.user, team=self.team
                ))

                inventory.total_quantity = quantity_after
                inventory.save(update_fields=['total_quantity'])
            else:
                InventoryFlow.objects.bulk_create(inventory_flows)
        else:
            # 作废入库单据
            stock_in_order = purchase_order.stock_in_order
            if stock_in_order.total_quantity != stock_in_order.remain_quantity:
                raise ValidationError(f'采购单据[{purchase_order.number}]无法作废, 已存在入库记录')

            stock_in_order.is_void = True
            stock_in_order.save(update_fields=['is_void'])

            # 作废入库商品
            stock_in_order.stock_in_goods_set.all().update(is_void=True)

        # 同步欠款
        supplier = purchase_order.supplier
        supplier.arrears_amount = NP.minus(supplier.arrears_amount, purchase_order.arrears_amount)
        supplier.save(update_fields=['arrears_amount'])

        # 同步账户, 流水
        if payment_order := purchase_order.payment_order:
            # 作废付款单据
            payment_order.is_void = True
            payment_order.save(update_fields=['is_void'])

            # 作废付款账号
            payment_order.payment_accounts.all().update(is_void=True)

            finance_flows = []
            for payment_account in payment_order.payment_accounts.all():
                account = payment_account.account
                amount_before = account.balance_amount
                amount_change = payment_account.payment_amount
                amount_after = NP.plus(amount_before, amount_change)

                finance_flows.append(FinanceFlow(
                    account=payment_account.account, type=FinanceFlow.Type.VOID_PAYMENT,
                    amount_before=amount_before, amount_change=amount_change, amount_after=amount_after,
                    void_payment_order=payment_order, creator=self.user, team=self.team
                ))

                account.balance_amount = amount_after
                account.save(update_fields=['balance_amount'])
            else:
                FinanceFlow.objects.bulk_create(finance_flows)

        serializer = PurchaseOrderSerializer(instance=purchase_order)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


__all__ = [
    'PurchaseOrderViewSet',
]
