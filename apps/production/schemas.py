from extensions.serializers import *


class NumberResponse(Serializer):
    number = CharField(label='编号')


class ProductionStockInRequest(Serializer):
    warehouse = IntegerField(label='仓库')
    stock_in_quantity = FloatField(label='入库数量')


__all__ = [
    'NumberResponse', 'ProductionStockInRequest',
]
