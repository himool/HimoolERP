from extensions.models import *


class PurchaseOrder(Model):
    """采购单据"""

    number = CharField(max_length=32, verbose_name='编号')
    warehouse = ForeignKey('data.Warehouse', on_delete=PROTECT, related_name='purchase_orders', verbose_name='仓库')
    supplier = ForeignKey('data.Supplier', on_delete=PROTECT, related_name='purchase_orders', verbose_name='供应商')
    handler = ForeignKey('system.User', on_delete=PROTECT, related_name='purchase_orders', verbose_name='经手人')
    handle_time = DateTimeField(verbose_name='处理时间')
    remark = CharField(max_length=256, null=True, blank=True, verbose_name='备注')
    total_amount = AmountField(verbose_name='总金额')
    total_quantity = FloatField(verbose_name='总数量')
    is_void = BooleanField(default=False, verbose_name='作废状态')
    creator = ForeignKey('system.User', on_delete=PROTECT,
                         related_name='created_purchase_orders', verbose_name='创建人')
    create_time = DateTimeField(auto_now_add=True, verbose_name='创建时间')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='purchase_orders')

    class Meta:
        unique_together = [('number', 'team')]


class PurchaseGoods(Model):
    """采购商品"""

    purchase_order = ForeignKey('purchase.PurchaseOrder', on_delete=CASCADE,
                                related_name='purchase_goods_set', verbose_name='采购单据')
    goods = ForeignKey('goods.Goods', on_delete=PROTECT, related_name='purchase_goods_set', verbose_name='商品')
    purchase_quantity = FloatField(verbose_name='采购数量')
    purchase_price = AmountField(verbose_name='采购单价')
    total_amount = AmountField(verbose_name='总金额')
    return_quantity = FloatField(default=0, verbose_name='退货数量')
    is_void = BooleanField(default=False, verbose_name='作废状态')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='purchase_goods_set')

    class Meta:
        unique_together = [('purchase_order', 'goods')]


class PurchaseReturnOrder(Model):
    """采购退货单据"""

    number = CharField(max_length=32, verbose_name='编号')
    purchase_order = ForeignKey('purchase.PurchaseOrder', on_delete=CASCADE, null=True,
                                related_name='purchase_return_orders', verbose_name='采购单据')
    warehouse = ForeignKey('data.Warehouse', on_delete=PROTECT, related_name='purchase_return_orders', verbose_name='仓库')
    supplier = ForeignKey('data.Supplier', on_delete=PROTECT, related_name='purchase_return_orders', verbose_name='供应商')
    handler = ForeignKey('system.User', on_delete=PROTECT, related_name='purchase_return_orders', verbose_name='经手人')
    handle_time = DateTimeField(verbose_name='处理时间')
    remark = CharField(max_length=256, null=True, blank=True, verbose_name='备注')
    total_amount = AmountField(verbose_name='总金额')
    total_quantity = FloatField(verbose_name='总数量')
    is_void = BooleanField(default=False, verbose_name='作废状态')
    creator = ForeignKey('system.User', on_delete=PROTECT,
                         related_name='created_purchase_return_orders', verbose_name='创建人')
    create_time = DateTimeField(auto_now_add=True, verbose_name='创建时间')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='purchase_return_orders')

    class Meta:
        unique_together = [('number', 'team')]


class PurchaseReturnGodos(Model):
    """采购退货商品"""

    purchase_return_order = ForeignKey('purchase.PurchaseReturnOrder', on_delete=CASCADE,
                                       related_name='purchase_return_goods_set', verbose_name='采购退货单据')
    goods = ForeignKey('goods.Goods', on_delete=PROTECT, related_name='purchase_return_goods_set', verbose_name='商品')
    return_quantity = FloatField(verbose_name='退货数量')
    return_price = AmountField(verbose_name='退货单价')
    total_amount = AmountField(verbose_name='总金额')
    is_void = BooleanField(default=False, verbose_name='作废状态')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='purchase_return_goods_set')

    class Meta:
        unique_together = [('purchase_return_order', 'goods')]


__all__ = [
    'PurchaseOrder', 'PurchaseGoods',
    'PurchaseReturnOrder', 'PurchaseReturnGodos',
]
