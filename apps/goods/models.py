from extensions.common.base import *
from extensions.models import *


class GoodsCategory(Model):
    """商品分类"""

    name = CharField(max_length=64, verbose_name='名称')
    remark = CharField(max_length=256, null=True, blank=True, verbose_name='备注')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='goods_categories')

    class Meta:
        unique_together = [('name', 'team')]


class GoodsUnit(Model):
    """商品单位"""

    name = CharField(max_length=64, verbose_name='名称')
    remark = CharField(max_length=256, null=True, blank=True, verbose_name='备注')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='goods_units')

    class Meta:
        unique_together = [('name', 'team')]


class Goods(Model):
    """商品"""

    number = CharField(max_length=32, verbose_name='编号')
    name = CharField(max_length=64, verbose_name='名称')
    barcode = CharField(max_length=32, null=True, blank=True, verbose_name='条码')
    category = ForeignKey('goods.GoodsCategory', on_delete=SET_NULL, null=True,
                          related_name='goods_set', verbose_name='商品分类')
    unit = ForeignKey('goods.GoodsUnit', on_delete=SET_NULL, null=True,
                      related_name='goods_set', verbose_name='商品单位')
    spec = CharField(max_length=64, null=True, blank=True, verbose_name='规格')
    enable_batch_control = BooleanField(default=False, verbose_name='启用批次控制')
    shelf_life_days = IntegerField(null=True, verbose_name='保质期天数')
    shelf_life_warning_days = IntegerField(default=0, verbose_name='保质期预警天数')
    enable_inventory_warning = BooleanField(default=False, verbose_name='启用库存警告')
    inventory_upper = FloatField(null=True, verbose_name='库存上限')
    inventory_lower = FloatField(null=True, verbose_name='库存下限')
    purchase_price = FloatField(verbose_name='采购价')
    retail_price = FloatField(verbose_name='零售价')
    level_price1 = FloatField(verbose_name='等级价一')
    level_price2 = FloatField(verbose_name='等级价二')
    level_price3 = FloatField(verbose_name='等级价三')

    remark = CharField(max_length=256, null=True, blank=True, verbose_name='备注')
    is_active = BooleanField(default=True, verbose_name='激活状态')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='goods_set')

    class Meta:
        unique_together = [('number', 'team')]

    @classmethod
    def get_number(cls, team):
        instance = cls.objects.filter(team=team).last()

        try:
            result = re.match('^(.*?)([1-9]+)$', instance.number)
            number = result.group(1) + str(int(result.group(2)) + 1)
        except AttributeError:
            number = 'G000000000001'

        return number


class GoodsImage(Model):
    """商品图片"""

    goods = ForeignKey('goods.Goods', on_delete=SET_NULL, null=True,
                       related_name='goods_images', verbose_name='商品')
    file = ImageField(verbose_name='文件')
    name = CharField(max_length=256, verbose_name='文件名称')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='goods_images')


class Batch(Model):
    """批次"""

    number = CharField(max_length=32, verbose_name='编号')
    inventory = ForeignKey('goods.Inventory', on_delete=CASCADE, related_name='batchs', verbose_name='库存')
    warehouse = ForeignKey('data.Warehouse', on_delete=CASCADE, related_name='batchs', verbose_name='仓库')
    goods = ForeignKey('goods.Goods', on_delete=CASCADE, related_name='batchs', verbose_name='商品')
    initial_quantity = FloatField(default=0, verbose_name='初始库存')
    total_quantity = FloatField(verbose_name='批次数量')
    remain_quantity = FloatField(verbose_name='批次剩余数量')
    production_date = DateField(null=True, verbose_name='生产日期')
    shelf_life_days = IntegerField(null=True, verbose_name='保质期天数')
    expiration_date = DateField(null=True, verbose_name='过期日期')
    has_stock = BooleanField(default=True, verbose_name='库存状态')
    create_time = DateTimeField(auto_now_add=True, verbose_name='创建时间')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='batchs')

    class Meta:
        unique_together = [('number', 'warehouse', 'goods', 'team')]


class Inventory(Model):
    """库存"""

    warehouse = ForeignKey('data.Warehouse', on_delete=CASCADE, related_name='inventories', verbose_name='仓库')
    goods = ForeignKey('goods.Goods', on_delete=CASCADE, related_name='inventories', verbose_name='商品')
    initial_quantity = FloatField(default=0, verbose_name='初始库存')
    total_quantity = FloatField(default=0, verbose_name='库存总数')
    has_stock = BooleanField(default=False, verbose_name='库存状态')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='inventories')

    class Meta:
        unique_together = [('warehouse', 'goods', 'team')]


__all__ = [
    'GoodsCategory', 'GoodsUnit', 'Goods', 'GoodsImage',
    'Batch', 'Inventory',
]
