from extensions.models import *


class Goods(Model):
    """商品"""

    number = CharField(max_length=32, verbose_name='编号')
    name = CharField(max_length=64, verbose_name='名称')
    barcode = CharField(max_length=32, blank=True, null=True, verbose_name='条码')
    category = ForeignKey('data.GoodsCategory', on_delete=SET_NULL, null=True,
                          related_name='goods_set', verbose_name='商品分类')
    unit = ForeignKey('data.GoodsUnit', on_delete=SET_NULL, null=True,
                      related_name='goods_set', verbose_name='商品单位')
    spec = CharField(max_length=64, null=True, blank=True, verbose_name='商品规格')
    enable_shelf_life = BooleanField(default=False, verbose_name='启用保质期')
    shelf_life_days = IntegerField(default=0, verbose_name='保质期天数')
    shelf_life_warning_days = IntegerField(default=0, verbose_name='保质期预警天数')
    enable_inventory_warning = BooleanField(default=False, verbose_name='启用库存警告')
    inventory_upper = FloatField(null=True, verbose_name='库存上限')
    inventory_lower = FloatField(null=True, verbose_name='库存下限')
    purchase_price = AmountField(verbose_name='采购价')
    retail_price = AmountField(verbose_name='零售价')
    level_price1 = AmountField(verbose_name='等级价一')
    level_price2 = AmountField(verbose_name='等级价二')
    level_price3 = AmountField(verbose_name='等级价三')

    remark = CharField(max_length=256, null=True, blank=True, verbose_name='备注')
    order = IntegerField(default=100, verbose_name='顺序')
    is_active = BooleanField(default=True, verbose_name='激活状态')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='goods_set')

    class Meta:
        unique_together = [('number', 'team'), ('name', 'team')]


class Batch(Model):
    """批次"""

    number = CharField(max_length=32, verbose_name='编号')
    warehouse = ForeignKey('data.Warehouse', on_delete=CASCADE, related_name='batchs', verbose_name='仓库')
    goods = ForeignKey('goods.Goods', on_delete=CASCADE, related_name='batchs', verbose_name='商品')
    total_quantity = FloatField(verbose_name='批次数量')
    remain_quantity = FloatField(verbose_name='批次剩余数量')
    production_date = DateField(null=True, verbose_name='生产日期')
    shelf_life_days = IntegerField(default=0, verbose_name='保质期天数')
    expiration_date = DateField(null=True, verbose_name='过期日期')
    is_empty = BooleanField(default=False, verbose_name='库存状态')
    create_time = DateTimeField(auto_now_add=True, verbose_name='创建时间')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='batchs')

    class Meta:
        unique_together = [('number', 'warehouse', 'goods', 'team')]


class Inventory(Model):
    """库存"""

    warehouse = ForeignKey('data.Warehouse', on_delete=CASCADE, related_name='inventories', verbose_name='仓库')
    goods = ForeignKey('goods.Goods', on_delete=CASCADE, related_name='inventories', verbose_name='商品')
    total_quantity = FloatField(default=0, verbose_name='库存总数')
    is_empty = BooleanField(default=True, verbose_name='库存状态')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='inventories')

    class Meta:
        unique_together = [('warehouse', 'goods', 'team')]


__all__ = [
    'Goods', 'Batch', 'Inventory',
]
