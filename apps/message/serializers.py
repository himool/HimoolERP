from extensions.common.base import *
from extensions.serializers import *
from extensions.exceptions import *
from apps.goods.models import *
from apps.sales.models import *
from apps.stock_in.models import *
from apps.stock_out.models import *


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
        fields = ['id', 'warehouse', 'warehouse_number', 'warehouse_name', 'goods', 'goods_number',
                  'goods_name', 'goods_barcode', 'unit_name', 'total_quantity', 'sales_quantity',
                  'start_time', 'end_time']


class StockInOrderReminderSerializer(BaseSerializer):
    """入库任务提醒"""

    warehouse_number = CharField(source='warehouse.number', read_only=True, label='仓库编号')
    warehouse_name = CharField(source='warehouse.name', read_only=True, label='仓库名称')

    class Meta:
        model = StockInOrder
        fields = ['id', 'number', 'warehouse', 'warehouse_number', 'warehouse_name',
                  'total_quantity', 'remain_quantity']


class StockOutOrderReminderSerializer(BaseSerializer):
    """出库任务提醒"""

    warehouse_number = CharField(source='warehouse.number', read_only=True, label='仓库编号')
    warehouse_name = CharField(source='warehouse.name', read_only=True, label='仓库名称')

    class Meta:
        model = StockOutOrder
        fields = ['id', 'number', 'warehouse', 'warehouse_number', 'warehouse_name',
                  'total_quantity', 'remain_quantity']


__all__ = [
    'SalesTaskReminderSerializer',
    'StockInOrderReminderSerializer', 'StockOutOrderReminderSerializer',
]
