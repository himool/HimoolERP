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


class SalesReportParameter(Serializer):
    start_date = DateField(required=True, label='开始日期')
    end_date = DateField(required=True, label='结束日期')
    category = IntegerField(required=False, label='商品分类')


class SalesReportStatisticResponse(Serializer):
    total_count = IntegerField(label='销售次数')
    total_quantity = FloatField(label='销售数量')
    total_amount = AmountField(label='销售金额')


class SalesReportGroupByGoodsResponse(Serializer):
    goods = CharField(label='商品ID')
    goods_number = CharField(label='商品编号')
    goods_name = CharField(label='商品名称')
    goods_barcode = CharField(label='商品条码')
    goods_spec = CharField(label='商品规格')
    category_name = CharField(label='分类名称')
    unit_name = CharField(label='单位名称')
    total_sales_quantity = FloatField(label='销售总数量')
    total_sales_amount = AmountField(label='销售总金额')
    min_sales_price = FloatField(label='最低销售价')
    avg_sales_price = FloatField(label='平均销售价')
    max_sales_price = FloatField(label='最高销售价')


__all__ = [
    'PurchaseReportParameter', 'PurchaseReportStatisticResponse', 'PurchaseReportGroupByGoodsResponse',
    'SalesReportParameter', 'SalesReportStatisticResponse', 'SalesReportGroupByGoodsResponse',
]
