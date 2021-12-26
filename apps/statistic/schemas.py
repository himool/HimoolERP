from extensions.common.schema import *
from extensions.serializers import *


class PurchaseReportParameter(Serializer):
    start_date = DateField(required=True, label='开始日期')
    end_date = DateField(required=True, label='结束日期')
    category = IntegerField(required=False, label='商品分类')


class PurchaseReportStatisticResponse(Serializer):
    total_count = IntegerField(label='采购次数')
    total_quantity = FloatField(label='采购数量')
    total_amount = AmountField(label='采购金额')


class PurchaseReportGroupByGoodsResponse(Serializer):
    goods = CharField(label='商品ID')
    goods_number = CharField(label='商品编号')
    goods_name = CharField(label='商品名称')
    goods_barcode = CharField(label='商品条码')
    goods_spec = CharField(label='商品规格')
    category_name = CharField(label='分类名称')
    unit_name = CharField(label='单位名称')
    total_purchase_quantity = FloatField(label='采购总数量')
    total_purchase_amount = AmountField(label='采购总金额')
    min_purchase_price = FloatField(label='最低采购价')
    avg_purchase_price = FloatField(label='平均采购价')
    max_purchase_price = FloatField(label='最高采购价')


__all__ = [
    'PurchaseReportParameter', 'PurchaseReportStatisticResponse', 'PurchaseReportGroupByGoodsResponse',
]
