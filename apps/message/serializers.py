from extensions.common.base import *
from extensions.serializers import *
from extensions.exceptions import *
from apps.goods.models import *


class InventoryMessageSerializer(BaseSerializer):
    """库存预警"""

    goods_number = CharField(source='goods.number', read_only=True, label='商品编号')
    goods_name = CharField(source='goods.name', read_only=True, label='商品名称')
    goods_barcode = CharField(source='goods.barcode', read_only=True, label='商品条码')
    unit_name = CharField(source='goods.unit.name', read_only=True, label='单位名称')
    inventory_upper = FloatField(source='goods.inventory_upper', read_only=True, label='库存上限')
    inventory_lower = FloatField(source='goods.inventory_lower', read_only=True, label='库存下限')

    class Meta:
        model = Inventory
        fields = ['goods', 'goods_number', 'goods_name', 'goods_barcode', 'total_quantity',
                  'unit_name', 'inventory_upper', 'inventory_lower']


__all__ = [
    'InventoryMessageSerializer',
]
