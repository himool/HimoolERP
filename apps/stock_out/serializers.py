from extensions.serializers import *
from extensions.exceptions import *
from apps.stock_out.models import *


class StockOutOrderSerializer(BaseSerializer):
    """出库单据"""

    class StockOutGoodsSerializer(BaseSerializer):
        """出库商品"""

        goods_number = CharField(source='goods.number', read_only=True, label='商品编号')
        goods_name = CharField(source='goods.name', read_only=True, label='商品名称')
        goods_barcode = CharField(source='goods.barcode', read_only=True, label='商品条码')
        unit_name = CharField(source='goods.unit.name', read_only=True, label='单位名称')

        class Meta:
            model = StockOutGoods
            fields = ['id', 'goods', 'goods_number', 'goods_name', 'goods_barcode',
                      'stock_in_quantity', 'remain_quantity', 'unit_name', 'is_completed']

    warehouse_number = CharField(source='warehouse.number', read_only=True, label='仓库编号')
    warehouse_name = CharField(source='warehouse.name', read_only=True, label='仓库名称')
    type_display = CharField(source='get_type_display', read_only=True, label='入库类型')
    sales_order_number = CharField(source='sales_order.number', read_only=True, label='采购单据编号')
    purchase_return_order_number = CharField(source='purchase_return_order.number', read_only=True, label='销售退货单据编号')
    creator_name = CharField(source='creator.name', read_only=True, label='创建人名称')
    stock_out_goods_items = StockOutGoodsSerializer(source='stock_in_goods_set', many=True, label='入库单据商品')

    class Meta:
        model = StockOutOrder
        fields = ['id', 'number', 'warehouse', 'warehouse_number', 'warehouse_name', 'type',
                  'type_display', 'sales_order', 'sales_order_number', 'purchase_return_order',
                  'purchase_return_order_number', 'total_quantity', 'remain_quantity', 'is_completed',
                  'is_void', 'creator', 'creator_name', 'create_time', 'stock_out_goods_items']


__all__ = [

]
