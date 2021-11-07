from extensions.models import *


class StockTransferOrder(Model):
    """调拨单据"""

    number = CharField(max_length=32, verbose_name='编号')
    out_warehouse = ForeignKey('data.Warehouse', on_delete=PROTECT,
                               related_name='out_stock_transfer_orders', verbose_name='出库仓库')
    in_warehouse = ForeignKey('data.Warehouse', on_delete=PROTECT,
                              related_name='in_stock_transfer_orders', verbose_name='入库仓库')
    handler = ForeignKey('system.User', on_delete=PROTECT, related_name='stock_transfer_orders', verbose_name='经手人')
    handle_time = DateTimeField(verbose_name='处理时间')
    remark = CharField(max_length=256, null=True, blank=True, verbose_name='备注')
    total_quantity = FloatField(verbose_name='调拨总数量')
    is_void = BooleanField(default=False, verbose_name='作废状态')
    creator = ForeignKey('system.User', on_delete=PROTECT,
                         related_name='created_stock_transfer_orders', verbose_name='创建人')
    create_time = DateTimeField(auto_now_add=True, verbose_name='创建时间')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='stock_transfer_orders')

    class Meta:
        unique_together = [('number', 'team')]


class StockTransferGoods(Model):
    """调拨商品"""

    stock_transfer_order = ForeignKey('stock_transfer.StockTransferOrder', on_delete=CASCADE,
                                      related_name='stock_transfer_goods_set', verbose_name='采购单据')
    goods = ForeignKey('goods.Goods', on_delete=PROTECT, related_name='stock_transfer_goods_set', verbose_name='商品')
    batch = ForeignKey('goods.Batch', on_delete=SET_NULL, null=True,
                       related_name='stock_transfer_goods_set', verbose_name='批次')
    stock_transfer_quantity = FloatField(verbose_name='调拨数量')
    is_void = BooleanField(default=False, verbose_name='作废状态')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='stock_transfer_goods_set')

    class Meta:
        unique_together = [('stock_transfer_order', 'goods', 'batch')]


__all__ = [
    'StockTransferOrder', 'StockTransferGoods',
]
