from extensions.models import *


class ProductionOrder(Model):
    """生产单据"""

    number = CharField(max_length=32, verbose_name='编号')
    is_related = BooleanField(default=False, verbose_name='关联状态')
    sales_order = ForeignKey('sales.SalesOrder', on_delete=PROTECT, null=True, related_name='production_orders', verbose_name='销售单')
    goods = ForeignKey('goods.Goods', on_delete=PROTECT, related_name='production_orders', verbose_name='产品')
    total_quantity = FloatField(verbose_name='生产总数')
    remain_quantity = FloatField(verbose_name='剩余数量')
    start_time = DateTimeField(null=True, verbose_name='开始时间')
    end_time = DateTimeField(null=True, verbose_name='结束时间')
    creator = ForeignKey('system.User', on_delete=PROTECT,
                         related_name='created_production_orders', verbose_name='创建人')
    create_time = DateTimeField(auto_now_add=True, verbose_name='创建时间')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='production_orders')


class ProductionRecord(Model):
    """生产记录"""

    production_order = ForeignKey('production.ProductionOrder', on_delete=CASCADE, related_name='production_records', verbose_name='生产单')
    goods = ForeignKey('goods.Goods', on_delete=PROTECT, related_name='production_records', verbose_name='产品')
    production_quantity = FloatField(verbose_name='生产数量')
    creator = ForeignKey('system.User', on_delete=PROTECT,
                         related_name='created_production_records', verbose_name='创建人')
    create_time = DateTimeField(auto_now_add=True, verbose_name='创建时间')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='production_records')


__all__ = [
    'ProductionOrder', 'ProductionRecord',
]
