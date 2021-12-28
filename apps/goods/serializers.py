from extensions.common.base import *
from extensions.serializers import *
from extensions.exceptions import *
from apps.goods.models import *
from apps.data.models import *


class GoodsCategorySerializer(BaseSerializer):

    class Meta:
        model = GoodsCategory
        read_only_fields = ['id']
        fields = ['name', 'remark', *read_only_fields]

    def validate_name(self, value):
        self.validate_unique({'name': value}, message=f'名称[{value}]已存在')
        return value


class GoodsCategoryExportSerializer(BaseSerializer):
    name = CharField(label='商品分类名称')
    remark = CharField(label='备注')

    class Meta:
        model = GoodsCategory
        fields = ['name', 'remark']


class GoodsCategoryImportSerializer(BaseSerializer):
    name = CharField(label='商品分类名称(必填)')
    remark = CharField(required=False, label='备注')

    class Meta:
        model = GoodsCategory
        fields = ['name', 'remark']


class GoodsUnitSerializer(BaseSerializer):

    class Meta:
        model = GoodsUnit
        read_only_fields = ['id']
        fields = ['name', 'remark', *read_only_fields]

    def validate_name(self, value):
        self.validate_unique({'name': value}, message=f'名称[{value}]已存在')
        return value


class GoodsUnitExportSerializer(BaseSerializer):
    name = CharField(label='商品单位名称')
    remark = CharField(label='备注')

    class Meta:
        model = GoodsUnit
        fields = ['name', 'remark']


class GoodsUnitImportSerializer(BaseSerializer):
    name = CharField(label='商品单位名称(必填)')
    remark = CharField(required=False, label='备注')

    class Meta:
        model = GoodsUnit
        fields = ['name', 'remark']


class GoodsSerializer(BaseSerializer):

    class InventoryItemSerializer(BaseSerializer):

        class BatchItemSerializer(BaseSerializer):
            id = IntegerField(required=False, label='批次ID')

            class Meta:
                model = Batch
                read_only_fields = ['total_quantity', 'remain_quantity']
                fields = ['id', 'number', 'initial_quantity', 'production_date', *read_only_fields]

            def validate_initial_quantity(self, value):
                if value < 0:
                    raise ValidationError('初始库存数量小于零')
                return value

        warehouse_number = CharField(source='warehouse.number', read_only=True, label='仓库编号')
        warehouse_name = CharField(source='warehouse.name', read_only=True, label='仓库名称')
        batch_items = BatchItemSerializer(source='batchs', required=False, many=True, label='批次Item')

        class Meta:
            model = Inventory
            read_only_fields = ['id', 'warehouse_number', 'warehouse_name']
            fields = ['warehouse', 'initial_quantity', 'batch_items', *read_only_fields]

        def validate_warehouse(self, instance):
            instance = self.validate_foreign_key(Warehouse, instance, message='仓库不存在')
            return instance

        def validate_initial_quantity(self, value):
            if value < 0:
                raise ValidationError('库存数量小于零')
            return value

    class GoodsImageItemSerializer(BaseSerializer):

        class Meta:
            model = GoodsImage
            fields = ['id', 'name', 'file']

    category_name = CharField(source='category.name', read_only=True, label='分类名称')
    unit_name = CharField(source='unit.name', read_only=True, label='单位名称')
    inventory_items = InventoryItemSerializer(
        source='inventories', required=False, many=True, label='库存Item')
    goods_image_items = GoodsImageItemSerializer(
        source='goods_images', many=True, read_only=True, label='商品图片Item')

    class Meta:
        model = Goods
        read_only_fields = ['id', 'category_name', 'unit_name', 'goods_image_items']
        fields = ['number', 'name', 'barcode', 'category', 'unit', 'spec', 'enable_batch_control',
                  'shelf_life_days', 'shelf_life_warning_days', 'enable_inventory_warning',
                  'inventory_upper', 'inventory_lower', 'purchase_price', 'retail_price',
                  'level_price1', 'level_price2', 'level_price3', 'remark', 'order',
                  'is_active', 'inventory_items', 'goods_images', *read_only_fields]
        extra_kwargs = {'goods_images': {'required': False}}

    def validate_number(self, value):
        self.validate_unique({'number': value}, message=f'编号[{value}]已存在')
        return value

    def validate_category(self, instance):
        instance = self.validate_foreign_key(GoodsCategory, instance, message='商品分类不存在')
        return instance

    def validate_unit(self, instance):
        instance = self.validate_foreign_key(GoodsUnit, instance, message='商品单位不存在')
        return instance

    def validate_enable_batch_control(self, value):
        if value and (self.team.enable_auto_stock_in or self.team.enable_auto_stock_out):
            raise ValidationError('只有同时关闭自动入库、自动出库, 才可以开启商品的批次控制')
        return value

    def validate_goods_images(self, instances):
        instances = self.validate_foreign_key_set(GoodsImage, instances, message='商品图片不存在')
        return instances

    @transaction.atomic
    def create(self, validated_data):
        inventory_items = validated_data.pop('inventories', [])
        goods = super().create(validated_data)

        # 同步库存
        batchs = []
        for warehouse in Warehouse.objects.filter(team=self.team):
            for inventory_item in inventory_items:
                if warehouse == inventory_item['warehouse']:
                    inventory_initial_quantity = inventory_item.get('initial_quantity', 0)
                    has_stock = inventory_initial_quantity > 0
                    inventory = Inventory.objects.create(
                        warehouse=warehouse, goods=goods, initial_quantity=inventory_initial_quantity,
                        total_quantity=inventory_initial_quantity, has_stock=has_stock, team=self.team
                    )

                    total_initial_quantity = 0

                    # 商品开启批次控制, 创建批次
                    batch_items = inventory_item.get('batchs')
                    if goods.enable_batch_control and batch_items:
                        for batch_item in batch_items:
                            batch_initial_quantity = batch_item.get('initial_quantity', 0)
                            production_date = batch_item.get('production_date')
                            expiration_date = None
                            if production_date and goods.shelf_life_days:
                                expiration_date = pendulum.parse(str(production_date)) \
                                    .add(days=goods.shelf_life_days).to_date_string()

                            has_stock = batch_initial_quantity > 0
                            batchs.append(Batch(
                                number=batch_item['number'], inventory=inventory, warehouse=warehouse,
                                goods=goods, initial_quantity=batch_initial_quantity,
                                total_quantity=batch_initial_quantity, remain_quantity=batch_initial_quantity,
                                production_date=production_date, shelf_life_days=goods.shelf_life_days,
                                expiration_date=expiration_date, has_stock=has_stock, team=self.team
                            ))

                            total_initial_quantity = NP.plus(total_initial_quantity, batch_initial_quantity)
                        else:
                            if total_initial_quantity != inventory_initial_quantity:
                                inventory.initial_quantity = total_initial_quantity
                                inventory.total_quantity = total_initial_quantity
                                inventory.has_stock = inventory.total_quantity > 0
                                inventory.save(update_fields=['initial_quantity', 'total_quantity', 'has_stock'])
                    break
            else:
                Inventory.objects.create(warehouse=warehouse, goods=goods, team=self.team)
        else:
            Batch.objects.bulk_create(batchs)

        return goods

    @transaction.atomic
    def update(self, instance, validated_data):
        inventory_items = validated_data.pop('inventories', [])
        goods = super().update(instance, validated_data)

        # 同步批次
        enable_batch_control = validated_data.get('enable_batch_control')
        if enable_batch_control is not None:
            if enable_batch_control != goods.enable_batch_control:
                if enable_batch_control:
                    batch_number = 'B' + pendulum.today().format('YYYYMMDD')
                    batchs = []
                    for inventory in Inventory.objects.filter(goods=goods, has_stock=True, team=self.team):
                        batchs.append(Batch(
                            number=batch_number, inventory=inventory, warehouse=inventory.warehouse,
                            goods=inventory.goods, total_quantity=inventory.total_quantity,
                            remain_quantity=inventory.total_quantity,
                            shelf_life_days=goods.shelf_life_days, team=self.team
                        ))
                    else:
                        Batch.objects.bulk_create(batchs)
                else:
                    instance.batchs.all().delete()

        # 同步库存
        create_batchs = []
        update_batchs = []
        for inventory in Inventory.objects.filter(goods=goods, team=self.team):
            for inventory_item in inventory_items:
                warehouse = inventory.warehouse
                if warehouse == inventory_item['warehouse']:
                    inventory_initial_quantity = inventory_item.get('initial_quantity', 0)

                    if goods.enable_batch_control:
                        total_initial_quantity = 0
                        batch_items = inventory_item.get('batchs', [])
                        for batch_item in batch_items:
                            batch_initial_quantity = batch_item.get('initial_quantity', 0)
                            production_date = batch_item.get('production_date')
                            expiration_date = None
                            if production_date and goods.shelf_life_days:
                                expiration_date = pendulum.parse(str(production_date)) \
                                    .add(days=goods.shelf_life_days).to_date_string()

                            if batch_id := batch_item.get('id'):
                                batch = Batch.objects.filter(id=batch_id, warehouse=warehouse,
                                                             goods=goods, team=self.team).first()
                                if not batch:
                                    batch_number = batch_item['number']
                                    raise ValidationError(f'批次[{batch_number}]不存在')

                                batch.number = batch_item['number']
                                batch.total_quantity = NP.minus(batch.total_quantity, batch.initial_quantity)
                                batch.remain_quantity = NP.minus(batch.remain_quantity, batch.initial_quantity)
                                batch.initial_quantity = batch_initial_quantity
                                batch.total_quantity = NP.plus(batch.total_quantity, batch.initial_quantity)
                                batch.remain_quantity = NP.plus(batch.remain_quantity, batch.initial_quantity)
                                batch.production_date = production_date
                                batch.expiration_date = expiration_date
                                batch.has_stock = batch.total_quantity > 0

                                update_batchs.append(batch)
                            else:
                                if Batch.objects.filter(number=batch_item['number'], warehouse=warehouse,
                                                        goods=goods, team=self.team).exists():
                                    batch_number = batch_item['number']
                                    raise ValidationError(f'批次[{batch_number}]已存在')

                                has_stock = batch_initial_quantity > 0
                                create_batchs.append(Batch(
                                    number=batch_item['number'], inventory=inventory, warehouse=warehouse,
                                    goods=goods, initial_quantity=batch_initial_quantity,
                                    total_quantity=batch_initial_quantity, remain_quantity=batch_initial_quantity,
                                    production_date=production_date, shelf_life_days=goods.shelf_life_days,
                                    expiration_date=expiration_date, has_stock=has_stock, team=self.team,
                                ))

                            total_initial_quantity = NP.plus(total_initial_quantity, batch_initial_quantity)
                        else:
                            inventory.total_quantity = NP.minus(inventory.total_quantity, inventory.initial_quantity)
                            inventory.initial_quantity = total_initial_quantity
                            inventory.total_quantity = NP.plus(inventory.total_quantity, inventory.initial_quantity)
                            inventory.has_stock = inventory.total_quantity > 0
                            inventory.save(update_fields=['initial_quantity', 'total_quantity', 'has_stock'])
                    else:
                        inventory.total_quantity = NP.minus(inventory.total_quantity, inventory.initial_quantity)
                        inventory.initial_quantity = inventory_initial_quantity
                        inventory.total_quantity = NP.plus(inventory.total_quantity, inventory.initial_quantity)
                        inventory.has_stock = inventory.total_quantity > 0
                        inventory.save(update_fields=['initial_quantity', 'total_quantity', 'has_stock'])

                    break
        else:
            Batch.objects.filter(goods=goods, team=self.team) \
                .exclude(id__in=[batch.id for batch in update_batchs]).delete()
            Batch.objects.bulk_create(create_batchs)
            Batch.objects.bulk_update(update_batchs,
                                      ['number', 'initial_quantity', 'total_quantity', 'remain_quantity',
                                       'production_date', 'expiration_date', 'has_stock'])

        return goods


class GoodsExportSerializer(BaseSerializer):
    number = CharField(label='编号')
    name = CharField(label='名称')
    barcode = CharField(label='条码')
    category_name = CharField(label='分类')
    unit_name = CharField(label='单位')
    spec = CharField(label='规格')
    enable_batch_control = BooleanField(label='启用批次控制[TRUE/FALSE]')
    shelf_life_days = IntegerField(label='保质期天数')
    shelf_life_warning_days = IntegerField(label='保质期预警天数')
    enable_inventory_warning = BooleanField(label='启用库存警告[TRUE/FALSE]')
    inventory_upper = FloatField(label='库存上限')
    inventory_lower = FloatField(label='库存下限')
    purchase_price = FloatField(label='采购价')
    retail_price = FloatField(label='零售价')
    level_price1 = FloatField(label='等级价一')
    level_price2 = FloatField(label='等级价二')
    level_price3 = FloatField(label='等级价三')
    remark = CharField(label='备注')
    order = IntegerField(label='排序')
    is_active = BooleanField(label='激活状态[TRUE/FALSE]')

    class Meta:
        model = Goods
        fields = ['number', 'name', 'barcode', 'category_name', 'unit_name', 'spec',
                  'enable_batch_control', 'shelf_life_days', 'shelf_life_warning_days',
                  'enable_inventory_warning', 'inventory_upper', 'inventory_lower',
                  'purchase_price', 'retail_price', 'level_price1', 'level_price2',
                  'level_price3', 'remark', 'order', 'is_active']


class GoodsImportSerializer(BaseSerializer):
    number = CharField(label='编号')
    name = CharField(label='名称')
    barcode = CharField(required=False, label='条码')
    category_name = CharField(required=False, label='分类')
    unit_name = CharField(required=False, label='单位')
    spec = CharField(required=False, label='规格')
    enable_batch_control = BooleanField(required=False, label='启用批次控制[TRUE/FALSE](默认: FALSE)')
    shelf_life_days = IntegerField(required=False, label='保质期天数')
    shelf_life_warning_days = IntegerField(required=False, label='保质期预警天数')
    enable_inventory_warning = BooleanField(required=False, label='启用库存警告[TRUE/FALSE](默认: FALSE)')
    inventory_upper = FloatField(required=False, label='库存上限')
    inventory_lower = FloatField(required=False, label='库存下限')
    purchase_price = FloatField(label='采购价')
    retail_price = FloatField(label='零售价')
    level_price1 = FloatField(label='等级价一')
    level_price2 = FloatField(label='等级价二')
    level_price3 = FloatField(label='等级价三')
    remark = CharField(required=False, label='备注')
    order = IntegerField(required=False, label='排序(默认: 100)')
    is_active = BooleanField(required=False, label='激活状态[TRUE/FALSE](默认: TRUE)')

    class Meta:
        model = Goods
        fields = ['number', 'name', 'barcode', 'category_name', 'unit_name', 'spec',
                  'enable_batch_control', 'shelf_life_days', 'shelf_life_warning_days',
                  'enable_inventory_warning', 'inventory_upper', 'inventory_lower',
                  'purchase_price', 'retail_price', 'level_price1', 'level_price2',
                  'level_price3', 'remark', 'order', 'is_active']

    def validate(self, attrs):
        if category_name := attrs.pop('category_name', None):
            goods_category = GoodsCategory.objects.filter(name=category_name, team=self.team).first()
            if not goods_category:
                raise ValidationError(f'商品分类[{category_name}]不存在')

            attrs['category'] = goods_category

        if unit_name := attrs.pop('unit_name', None):
            goods_unit = GoodsUnit.objects.filter(name=unit_name, team=self.team).first()
            if not goods_unit:
                raise ValidationError(f'商品分类[{unit_name}]不存在')

            attrs['unit'] = goods_unit

        return super().validate(attrs)


class GoodsImageSerializer(BaseSerializer):

    class Meta:
        model = GoodsImage
        read_only_fields = ['id', 'name']
        fields = ['file', *read_only_fields]

    def create(self, validated_data):
        validated_data['name'] = validated_data['file'].name
        return super().create(validated_data)


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
    'GoodsCategorySerializer', 'GoodsCategoryExportSerializer', 'GoodsCategoryImportSerializer',
    'GoodsUnitSerializer', 'GoodsUnitExportSerializer', 'GoodsUnitImportSerializer',
    'GoodsSerializer', 'GoodsExportSerializer', 'GoodsImportSerializer',
    'GoodsImageSerializer',
    'BatchSerializer', 'InventorySerializer',
]
