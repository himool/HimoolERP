from extensions.models import *


class StockCheckOrder(Model):
    """盘点单据"""

    class Status(TextChoices):
        """盘点状态"""

        SURPLUS = ('surplus', '盘盈')
        LOSS = ('loss', '盘亏')
        UNCHANGED = ('unchanged', '无变化')

    number = CharField(max_length=32, verbose_name='编号')
    warehouse = ForeignKey('data.Warehouse', on_delete=PROTECT, related_name='stock_check_orders', verbose_name='仓库')
    handler = ForeignKey('system.User', on_delete=PROTECT, related_name='stock_check_orders', verbose_name='经手人')
    handle_time = DateTimeField(verbose_name='处理时间')
    remark = CharField(max_length=256, null=True, blank=True, verbose_name='备注')
    status = CharField(max_length=32, choices=Status.choices, null=True, verbose_name='盘点状态')
    total_book_quantity = FloatField(verbose_name='账面总数量')
    total_actual_quantity = FloatField(verbose_name='实际总数量')
    total_surplus_quantity = AmountField(verbose_name='盘盈总金额')
    is_void = BooleanField(default=False, verbose_name='作废状态')
    creator = ForeignKey('system.User', on_delete=PROTECT,
                         related_name='created_stock_check_orders', verbose_name='创建人')
    create_time = DateTimeField(auto_now_add=True, verbose_name='创建时间')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='stock_check_orders')

    class Meta:
        unique_together = [('number', 'team')]


class StockCheckGoods(Model):
    """盘点商品"""

    class Status(TextChoices):
        """盘点状态"""

        SURPLUS = ('surplus', '盘盈')
        LOSS = ('loss', '盘亏')
        UNCHANGED = ('unchanged', '无变化')

    stock_check_order = ForeignKey('stock_check.StockCheckOrder', on_delete=CASCADE,
                                   related_name='stock_check_goods_set', verbose_name='盘点单据')
    goods = ForeignKey('goods.Goods', on_delete=PROTECT, related_name='stock_check_goods_set', verbose_name='商品')
    batch = ForeignKey('goods.Batch', on_delete=SET_NULL, null=True,
                       related_name='stock_check_goods_set', verbose_name='批次')
    book_quantity = FloatField(verbose_name='账面数量')
    actual_quantity = FloatField(verbose_name='实际数量')
    status = CharField(max_length=32, choices=Status.choices, verbose_name='盘点状态')
    surplus_quantity = FloatField(verbose_name='盘盈数量')
    purchase_price = AmountField(verbose_name='采购单价')
    surplus_amount = AmountField(verbose_name='盘盈金额')
    is_void = BooleanField(default=False, verbose_name='作废状态')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='stock_check_goods_set')

    class Meta:
        unique_together = [('stock_check_order', 'goods', 'batch')]


__all__ = [
    'StockCheckOrder', 'StockCheckGoods',
]
