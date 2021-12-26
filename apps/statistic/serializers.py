from extensions.common.base import *
from extensions.serializers import *
from extensions.exceptions import *
from apps.purchase.models import *


class PurchaseReportDetialSerializer(BaseSerializer):
    """采购明细"""

    goods_number = CharField(source='goods.number', read_only=True, label='商品编号')
    goods_name = CharField(source='goods.name', read_only=True, label='商品名称')
    goods_barcode = CharField(source='goods.barcode', read_only=True, label='商品条码')
    goods_spec = CharField(source='goods.spec', read_only=True, label='商品规格')
    category_name = CharField(source='goods.category.name', read_only=True, label='分类名称')
    unit_name = CharField(source='goods.unit.name', read_only=True, label='单位名称')
    purchase_order_number = CharField(source='purchase_order.number', read_only=True, label='采购单号')
    supplier_name = CharField(source='purchase_order.supplier.name', read_only=True, label='供应商名称')

    class Meta:
        model = PurchaseGoods
        fields = ['id', 'goods', 'goods_number', 'goods_name', 'goods_barcode', 'goods_spec',
                  'purchase_quantity', 'category_name', 'unit_name', 'purchase_price', 'total_amount',
                  'purchase_order', 'purchase_order_number', 'supplier_name']


__all__ = [
    'PurchaseReportDetialSerializer',
]
