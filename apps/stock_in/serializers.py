from apps.goods.models import Batch
from extensions.serializers import *
from extensions.exceptions import *
from apps.stock_in.models import *
from apps.system.models import *


class StockInTaskSerializer(BaseSerializer):
    """入库任务"""

    class StockInTaskGoodsSerializer(BaseSerializer):
        """入库任务商品"""

        goods_number = CharField(source='goods.number', read_only=True, label='商品编号')
        goods_name = CharField(source='goods.name', read_only=True, label='商品名称')
        goods_barcode = CharField(source='goods.barcode', read_only=True, label='商品条码')
        unit_name = CharField(source='goods.unit.name', read_only=True, label='单位名称')
        enable_batch_control = BooleanField(source='goods.enable_batch_control', read_only=True, label='启用批次控制')
        shelf_life_days = CharField(source='goods.shelf_life_days', read_only=True, label='保质期天数')

        class Meta:
            model = StockInGoods
            fields = ['goods', 'goods_number', 'goods_name', 'goods_barcode', 'stock_in_quantity',
                      'remain_quantity', 'unit_name', 'enable_batch_control', 'shelf_life_days', 'is_completed']

    warehouse_number = CharField(source='warehouse.number', read_only=True, label='仓库编号')
    warehouse_name = CharField(source='warehouse.name', read_only=True, label='仓库名称')
    type_display = CharField(source='get_type_display', read_only=True, label='入库类型')
    purchase_order_number = CharField(source='purchase_order.number', read_only=True, label='采购单据编号')
    sales_return_order_number = CharField(source='sales_return_order.number', read_only=True, label='销售退货单据编号')
    creator_name = CharField(source='creator.name', read_only=True, label='创建人名称')
    stock_in_task_goods_items = StockInTaskGoodsSerializer(source='stock_in_goods_set',  many=True, label='入库任务商品')

    class Meta:
        model = StockInOrder
        fields = ['id', 'number', 'warehouse', 'warehouse_number', 'warehouse_name', 'type',
                  'type_display', 'purchase_order', 'purchase_order_number', 'sales_return_order',
                  'sales_return_order_number', 'total_quantity', 'remain_quantity', 'is_completed',
                  'is_void', 'creator', 'creator_name', 'create_time', 'stock_in_task_goods_items']


class StockInRecordSerializer(BaseSerializer):
    """入库记录"""

    class StockInRecordGoodsSerializer(BaseSerializer):
        """入库记录商品"""

        goods_number = CharField(source='goods.number', read_only=True, label='商品编号')
        goods_name = CharField(source='goods.name', read_only=True, label='商品名称')
        goods_barcode = CharField(source='goods.barcode', read_only=True, label='商品条码')
        unit_name = CharField(source='goods.unit.name', read_only=True, label='单位名称')
        batch_number = CharField(source='batch.number', required=False, label='批次编号')

        class Meta:
            model = StockInRecordGoods
            read_only_fields = ['id', 'goods', 'goods_number', 'goods_name', 'goods_barcode', 'unit_name',
                                'enable_batch_control', 'shelf_life_days', 'expiration_date']
            fields = ['stock_in_goods', 'stock_in_quantity', 'production_date', 'batch_number', *read_only_fields]

        def validate_stock_in_goods(self, instance):
            instance = self.validate_foreign_key(StockInGoods, instance, message='入库商品不存在')
            if not instance.is_void:
                raise ValidationError(f'入库商品[{instance.goods.name}]已作废')

            if not instance.is_completed:
                raise ValidationError(f'入库商品[{instance.goods.name}]已完成')
            return instance

        def validate_stock_in_quantity(self, value):
            if value <= 0:
                raise ValidationError('采购数量小于或等于零')
            return value

        def validate(self, attrs):
            goods = attrs['stock_in_goods'].goods
            if goods.enable_batch_control:
                if not (attrs.get('batch') or attrs['batch'].get('number')):
                    raise ValidationError(f'商品[{goods.name}]批次编号为空')
            return super().validate(attrs)

    stock_in_order_number = CharField(source='stock_in_order.number', read_only=True, label='入库单据编号')
    warehouse_number = CharField(source='warehouse.number', read_only=True, label='仓库编号')
    warehouse_name = CharField(source='warehouse.name', read_only=True, label='仓库名称')
    creator_name = CharField(source='creator.name', read_only=True, label='创建人名称')
    stock_in_record_goods_items = StockInRecordGoodsSerializer(source='stock_in_record_goods_set',
                                                               many=True, label='入库记录商品')

    class Meta:
        model = StockInRecord
        read_only_fields = ['id', 'warehouse', 'warehouse_number', 'warehouse_name', 'total_quantity',
                            'is_void', 'creator', 'creator_name', 'create_time']
        fields = ['stock_in_order', 'handler', 'handle_time', 'remark', *read_only_fields]

    def validate_stock_in_order(self, instance):
        instance = self.validate_foreign_key(StockInOrder, instance, message='入库单据不存在')
        if not instance.is_void:
            raise ValidationError(f'入库单据[{instance.goods.name}]已作废')

        if not instance.is_completed:
            raise ValidationError(f'入库单据[{instance.goods.name}]已完成')
        return instance

    def validate_handler(self, instance):
        instance = self.validate_foreign_key(User, instance, message='经手人不存在')
        if not instance.is_active:
            raise ValidationError(f'经手人[{instance.name}]未激活')
        return instance

    @transaction.atomic
    def create(self, validated_data):
        stock_in_record_goods_items = validated_data.pop('stock_in_record_goods_set')

        stock_in_order = validated_data['stock_in_order']
        validated_data['warehouse'] = stock_in_order.warehouse
        validated_data['creator'] = self.user
        stock_in_record = super().create(validated_data)

        total_stock_in_quantity = 0

        # 创建入库记录商品
        stock_in_record_goods_set = []
        for stock_in_record_goods_item in stock_in_record_goods_items:
            stock_in_goods = stock_in_record_goods_item['stock_in_goods']
            stock_in_quantity = stock_in_record_goods_item['stock_in_quantity']
            goods = stock_in_goods.goods

            production_date = None
            expiration_date = None
            batch = None
            if goods.enable_batch_control:
                production_date = stock_in_record_goods_item.get('production_date')
                if production_date and goods.shelf_life_days:
                    expiration_date = pendulum.parse(str(production_date)).add(days=goods.shelf_life_days)

                # 创建批次
                batch = Batch.objects.create(
                    number=stock_in_record_goods_item['batch']['number'], warehouse=stock_in_record.warehouse,
                    goods=goods, total_quantity=stock_in_quantity, remain_quantity=stock_in_quantity,
                    production_date=production_date, shelf_life_days=goods.shelf_life_days,
                    expiration_date=expiration_date, team=self.team
                )

            stock_in_record_goods_set.append(StockInRecordGoods(
                stock_in_record=stock_in_record, stock_in_goods=stock_in_goods, goods=goods,
                stock_in_quantity=stock_in_quantity, enable_batch_control=goods.enable_batch_control,
                production_date=production_date, shelf_life_days=goods.shelf_life_days,
                expiration_date=expiration_date, batch=batch, team=self.team
            ))

            total_stock_in_quantity = NP.plus(total_stock_in_quantity, stock_in_quantity)
        else:
            StockInRecordGoods.objects.bulk_create(stock_in_record_goods_set)
            stock_in_record.total_quantity = total_stock_in_quantity
            stock_in_record.save(update_fields=['total_quantity'])

        return stock_in_record


__all__ = [
    'StockInTaskSerializer', 'StockInRecordSerializer',
]
