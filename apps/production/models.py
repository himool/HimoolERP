from extensions.models import *


class ProductionOrder(Model):
    """生产单据"""

    number = CharField(max_length=32, verbose_name='编号')
    is_related = BooleanField()
    sales_order = ForeignKey()
    warehouse = ForeignKey('data.Warehouse', on_delete=PROTECT, related_name='sales_orders', verbose_name='仓库')
    goods = ForeignKey()
    total_quantity = FloatField()
    start_time = DateTimeField()
    end_time = DateTimeField()
    creator = ForeignKey('system.User', on_delete=PROTECT,
                         related_name='created_sales_orders', verbose_name='创建人')
    create_time = DateTimeField(auto_now_add=True, verbose_name='创建时间')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='sales_orders')


class ProductionRecord(Model):
    """生产记录"""

    production_order = ForeignKey()
    warehouse = ForeignKey('data.Warehouse', on_delete=PROTECT, related_name='sales_orders', verbose_name='仓库')
    goods = ForeignKey()
    production_quantity = FloatField()
    creator = ForeignKey('system.User', on_delete=PROTECT,
                         related_name='created_sales_orders', verbose_name='创建人')
    create_time = DateTimeField(auto_now_add=True, verbose_name='创建时间')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='sales_orders')


__all__ = [
    'ProductionPlan', 'ProductionRecord',
]
