from extensions.common.base import *
from extensions.serializers import *
from extensions.exceptions import *
from apps.goods.models import *
from apps.sales.models import *


class InventoryWarningSerializer(BaseSerializer):
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


class SalesTaskReminderSerializer(BaseSerializer):
    """销售任务提醒"""

    warehouse_number = CharField(source='warehouse.number', read_only=True, label='仓库编号')
    warehouse_name = CharField(source='warehouse.name', read_only=True, label='仓库名称')
    goods_number = CharField(source='goods.number', read_only=True, label='商品编号')
    goods_name = CharField(source='goods.name', read_only=True, label='商品名称')
    goods_barcode = CharField(source='goods.barcode', read_only=True, label='商品条码')
    unit_name = CharField(source='goods.unit.name', read_only=True, label='单位名称')

    class Meta:
        model = SalesTask
        read_only_fields = ['id', 'warehouse_number', 'warehouse_name', 'goods_number', 'goods_name',
                            'goods_barcode', 'unit_name', 'salesperson_name', 'sales_quantity',
                            'is_completed', 'create_time']
        fields = ['warehouse', 'goods', 'salesperson', 'total_quantity', 'start_time', 'end_time',
                  *read_only_fields]


__all__ = [
    'InventoryWarningSerializer',
]
