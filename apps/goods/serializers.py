from extensions.serializers import *
from extensions.exceptions import *
from apps.goods.models import *
from apps.data.models import *


class GoodsSerializer(BaseSerializer):

    class InventorySerializer(BaseSerializer):
        warehouse_number = CharField(source='warehouse.number', read_only=True, label='仓库编号')
        warehouse_name = CharField(source='warehouse.name', read_only=True, label='仓库名称')

        class Meta:
            model = Inventory
            read_only_fields = ['id', 'warehouse_number', 'warehouse_name']
            fields = ['warehouse', 'initial_quantity', *read_only_fields]

    category_name = CharField(source='category.name', read_only=True, label='分类名称')
    unit_name = CharField(source='unit.name', read_only=True, label='单位名称')
    inventory_items = InventorySerializer(source='inventories', required=False, many=True, label='库存')

    class Meta:
        model = Goods
        read_only_fields = ['id', 'category_name', 'unit_name']
        fields = ['number', 'name', 'barcode', 'category', 'unit', 'spec', 'enable_batch_control',
                  'shelf_life_days', 'shelf_life_warning_days', 'enable_inventory_warning',
                  'inventory_upper', 'inventory_lower', 'purchase_price', 'retail_price',
                  'level_price1', 'level_price2', 'level_price3', 'remark', 'order',
                  'is_active', 'inventory_items', *read_only_fields]

    def validate_number(self, value):
        self.validate_unique({'number': value}, message=f'编号[{value}]已存在')
        return value

    def validate_name(self, value):
        self.validate_unique({'name': value}, message=f'名称[{value}]已存在')
        return value

    def validate_category(self, instance):
        instance = self.validate_foreign_key(GoodsCategory, instance, message='商品分类不存在')
        return instance

    def validate_unit(self, instance):
        instance = self.validate_foreign_key(GoodsUnit, instance, message='商品单位不存在')
        return instance

    @transaction.atomic
    def create(self, validated_data):
        inventory_items = validated_data.pop('inventories', [])
        goods = super().create(validated_data)

        # 同步库存
        inventories = []
        for warehouse in Warehouse.objects.filter(team=self.team):
            for inventory_item in inventory_items:
                if warehouse == inventory_item['warehouse']:
                    inventories.append(Inventory(
                        warehouse=warehouse, goods=goods,
                        initial_quantity=inventory_item['initial_quantity'],
                        total_quantity=inventory_item['initial_quantity'], team=self.team
                    ))
                    break
            else:
                inventories.append(Inventory(warehouse=warehouse, goods=goods, team=self.team))
        else:
            Inventory.objects.bulk_create(inventories)

        return goods

    @transaction.atomic
    def update(self, instance, validated_data):
        inventory_items = validated_data.pop('inventories', [])
        goods = super().update(instance, validated_data)

        # 同步批次
        if enable_batch_control := validated_data.get('enable_batch_control'):
            if enable_batch_control != instance.enable_batch_control:
                if enable_batch_control:
                    batch_number = 'B' + pendulum.today().format('YYYYMMDD')
                    batchs = []
                    for inventory in Inventory.objects.filter(goods=goods, has_stock=True, team=self.team):
                        batchs.append(Batch(
                            number=batch_number, warehouse=inventory.warehouse, goods=inventory.goods,
                            total_quantity=inventory.total_quantity, remain_quantity=inventory.total_quantity,
                            shelf_life_days=goods.shelf_life_days, team=self.team
                        ))
                    else:
                        Batch.objects.bulk_create(batchs)
                else:
                    instance.batchs.all().delete()

        # 同步库存
        for inventory in Inventory.objects.filter(goods=goods, team=self.team):
            for inventory_item in inventory_items:
                if (inventory.warehouse == inventory_item['warehouse'] and
                        inventory.initial_quantity != inventory_item['initial_quantity']):
                    inventory.total_quantity = NP.minus(inventory.total_quantity, inventory.initial_quantity)
                    inventory.initial_quantity = inventory_item['initial_quantity']
                    inventory.total_quantity = NP.plus(inventory.total_quantity, inventory.initial_quantity)
                    inventory.save(update_fields=['initial_quantity', 'total_quantity'])

        return goods


class BatchSerializer(BaseSerializer):
    warehouse_number = CharField(source='warehouse.number', read_only=True, label='仓库编号')
    warehouse_name = CharField(source='warehouse.name', read_only=True, label='仓库名称')
    goods_number = CharField(source='goods.number', read_only=True, label='商品编号')
    goods_name = CharField(source='goods.name', read_only=True, label='商品名称')
    goods_barcode = CharField(source='goods.barcode', read_only=True, label='商品条码')
    unit_name = CharField(source='goods.unit.name', read_only=True, label='单位名称')

    class Meta:
        model = Batch
        fields = ['id', 'number', 'warehouse', 'warehouse_number', 'warehouse_name', 'goods', 'goods_number',
                  'goods_name', 'goods_barcode', 'total_quantity', 'remain_quantity', 'unit_name',
                  'production_date', 'shelf_life_days', 'expiration_date', 'has_stock', 'create_time']


class InventorySerializer(BaseSerializer):
    warehouse_number = CharField(source='warehouse.number', read_only=True, label='仓库编号')
    warehouse_name = CharField(source='warehouse.name', read_only=True, label='仓库名称')
    goods_number = CharField(source='goods.number', read_only=True, label='商品编号')
    goods_name = CharField(source='goods.name', read_only=True, label='商品名称')
    goods_barcode = CharField(source='goods.barcode', read_only=True, label='商品条码')
    unit_name = CharField(source='goods.unit.name', read_only=True, label='单位名称')

    class Meta:
        model = Inventory
        fields = ['id', 'warehouse', 'warehouse_number', 'warehouse_name', 'goods', 'goods_number',
                  'goods_name', 'goods_barcode', 'total_quantity', 'unit_name', 'has_stock']


__all__ = [
    'GoodsSerializer', 'BatchSerializer', 'InventorySerializer',
]
