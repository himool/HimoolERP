from extensions.models import *


class SalesOrder(Model):
    """销售单据"""

    number = CharField(max_length=32, verbose_name='编号')
    warehouse = ForeignKey('data.Warehouse', on_delete=PROTECT, related_name='sales_orders', verbose_name='仓库')
    client = ForeignKey('data.Client', on_delete=PROTECT, related_name='sales_orders', verbose_name='客户')
    handler = ForeignKey('system.User', on_delete=PROTECT, related_name='sales_orders', verbose_name='经手人')
    handle_time = DateTimeField(verbose_name='处理时间')
    remark = CharField(max_length=256, null=True, blank=True, verbose_name='备注')
    discount = FloatField(default=100, verbose_name='折扣')
    total_amount = AmountField(verbose_name='总金额')
    total_quantity = FloatField(verbose_name='总数量')
    is_void = BooleanField(default=False, verbose_name='作废状态')
    creator = ForeignKey('system.User', on_delete=PROTECT,
                         related_name='created_sales_orders', verbose_name='创建人')
    create_time = DateTimeField(auto_now_add=True, verbose_name='创建时间')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='sales_orders')

    class Meta:
        unique_together = [('number', 'team')]


class SalesGoods(Model):
    """销售商品"""

    sales_order = ForeignKey('sales.SalesOrder', on_delete=CASCADE,
                             related_name='sales_goods_set', verbose_name='销售单据')
    goods = ForeignKey('goods.Goods', on_delete=PROTECT, related_name='sales_goods_set', verbose_name='商品')
    sales_quantity = FloatField(verbose_name='销售数量')
    sales_unit_price = AmountField(verbose_name='销售单价')
    total_amount = AmountField(verbose_name='总金额')
    return_quantity = FloatField(default=0, verbose_name='退货数量')
    is_void = BooleanField(default=False, verbose_name='作废状态')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='sales_goods_set')

    class Meta:
        unique_together = [('sales_order', 'goods')]


class SalesReturnOrder(Model):
    """销售退货单据"""

    number = CharField(max_length=32, verbose_name='编号')
    sales_order = ForeignKey('sales.SalesOrder', on_delete=CASCADE, null=True,
                             related_name='sales_return_orders', verbose_name='销售单据')
    warehouse = ForeignKey('data.Warehouse', on_delete=PROTECT, related_name='sales_return_orders', verbose_name='仓库')
    client = ForeignKey('data.Client', on_delete=PROTECT, related_name='sales_return_orders', verbose_name='客户')
    handler = ForeignKey('system.User', on_delete=PROTECT, related_name='sales_return_orders', verbose_name='经手人')
    handle_time = DateTimeField(verbose_name='处理时间')
    remark = CharField(max_length=256, null=True, blank=True, verbose_name='备注')
    total_amount = AmountField(verbose_name='总金额')
    total_quantity = FloatField(verbose_name='总数量')
    is_void = BooleanField(default=False, verbose_name='作废状态')
    creator = ForeignKey('system.User', on_delete=PROTECT,
                         related_name='created_sales_return_orders', verbose_name='创建人')
    create_time = DateTimeField(auto_now_add=True, verbose_name='创建时间')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='sales_return_orders')

    class Meta:
        unique_together = [('number', 'team')]


class SalesReturnGoods(Model):
    """销售退货商品"""

    sales_return_order = ForeignKey('sales.SalesReturnOrder', on_delete=CASCADE,
                                    related_name='sales_return_goods_set', verbose_name='销售退货单据')
    goods = ForeignKey('goods.Goods', on_delete=PROTECT, related_name='sales_return_goods_set', verbose_name='商品')
    return_quantity = FloatField(verbose_name='退货数量')
    return_unit_price = AmountField(verbose_name='退货单价')
    total_amount = AmountField(verbose_name='总金额')
    is_void = BooleanField(default=False, verbose_name='作废状态')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='sales_return_goods_set')

    class Meta:
        unique_together = [('sales_return_order', 'goods')]


class SalesTask(Model):
    """销售任务"""

    warehouse = ForeignKey('data.Warehouse', on_delete=CASCADE, related_name='sales_tasks', verbose_name='仓库')
    goods = ForeignKey('goods.Goods', on_delete=CASCADE, related_name='sales_tasks', verbose_name='商品')
    sales_quantity = FloatField(verbose_name='销售数量')
    start_time = DateTimeField(verbose_name='开始时间')
    end_time = DateTimeField(verbose_name='结束时间')
    create_time = DateTimeField(auto_now_add=True, verbose_name='创建时间')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='sales_tasks')


__all__ = [
    'SalesOrder', 'SalesGoods',
    'SalesReturnOrder', 'SalesReturnGoods',
    'SalesTask',
]
