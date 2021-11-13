from extensions.serializers import *
from extensions.exceptions import *
from apps.sales.models import *
from apps.data.models import *
from apps.goods.models import *
from apps.system.models import *
from apps.finance.models import *


class SalesOrderSerializer(BaseSerializer):
    """销售单据"""

    class SalesGoodsSerializer(BaseSerializer):
        """销售商品"""

        goods_number = CharField(source='goods.number', read_only=True, label='商品编号')
        goods_name = CharField(source='goods.name', read_only=True, label='商品名称')
        goods_barcode = CharField(source='goods.barcode', read_only=True, label='商品条码')
        unit_name = CharField(source='goods.unit.name', read_only=True, label='单位名称')

        class Meta:
            model = SalesGoods
            read_only_fields = ['id', 'goods_number', 'goods_name', 'goods_barcode', 'total_amount',
                                'return_quantity', 'unit_name']
            fields = ['goods', 'sales_quantity', 'sales_price', *read_only_fields]

        def validate_goods(self, instance):
            instance = self.validate_foreign_key(Goods, instance, message='商品不存在')
            if not instance.is_active:
                raise ValidationError(f'商品[{instance.name}]未激活')
            return instance

        def validate_sales_quantity(self, value):
            if value <= 0:
                raise ValidationError('销售数量小于或等于零')
            return value

        def validate_sales_price(self, value):
            if value <= 0:
                raise ValidationError('销售单价小于或等于零')
            return value

    class CollectionAccountSerializer(BaseSerializer):
        """收款账户"""

        account_number = CharField(source='account.number', read_only=True, label='账户编号')
        account_name = CharField(source='account.name', read_only=True, label='账户名称')

        class Meta:
            model = CollectionAccount
            read_only_fields = ['id', 'account_number', 'account_name']
            fields = ['account', 'collection_amount', *read_only_fields]

        def validate_account(self, instance):
            instance = self.validate_foreign_key(Account, instance, message='账户不存在')
            if not instance.is_active:
                raise ValidationError(f'账户[{instance.name}]未激活')
            return instance

        def validate_collection_amount(self, value):
            if value <= 0:
                raise ValidationError('收款金额小于或等于零')
            return value

    warehouse_number = CharField(source='warehouse.number', read_only=True, label='仓库编号')
    warehouse_name = CharField(source='warehouse.name', read_only=True, label='仓库名称')
    client_number = CharField(source='client.number', read_only=True, label='客户编号')
    client_name = CharField(source='client.name', read_only=True, label='客户名称')
    handler_name = CharField(source='handler.name', read_only=True, label='经手人名称')
    creator_name = CharField(source='creator.name', read_only=True, label='创建人名称')
    sales_goods_items = SalesGoodsSerializer(source='sales_goods_set', many=True, label='销售商品')
    collection_account_items = CollectionAccountSerializer(source='collection_order.collection_accounts',
                                                           required=False, many=True, label='收款账户')

    class Meta:
        model = SalesOrder
        read_only_fields = ['id', 'warehouse_number', 'warehouse_name', 'client_number', 'client_name',
                            'handler_name', 'total_quantity', 'total_amount', 'collection_amount',
                            'arrears_amount', 'is_void', 'enable_auto_stock_out', 'creator',
                            'creator_name', 'create_time']
        fields = ['number', 'warehouse', 'client', 'handler', 'handle_time', 'discount', 'other_amount',
                  'remark', 'sales_goods_items', 'collection_account_items', *read_only_fields]

    def validate_number(self, value):
        self.validate_unique({'number': value}, message=f'编号[{value}]已存在')
        return value

    def validate_warehouse(self, instance):
        instance = self.validate_foreign_key(Warehouse, instance, message='仓库不存在')
        if not instance.is_active:
            raise ValidationError(f'仓库[{instance.name}]未激活')

        if not instance.is_locked:
            raise ValidationError(f'仓库[{instance.name}]已锁定')
        return instance

    def validate_client(self, instance):
        instance = self.validate_foreign_key(Client, instance, message='客户不存在')
        if not instance.is_active:
            raise ValidationError(f'客户[{instance.name}]未激活')
        return instance

    def validate_handler(self, instance):
        instance = self.validate_foreign_key(User, instance, message='经手人不存在')
        if not instance.is_active:
            raise ValidationError(f'经手人[{instance.name}]未激活')
        return instance

    def validate_other_amount(self, value):
        if value <= 0:
            raise ValidationError('其他费用小于或等于零')
        return value

    @transaction.atomic
    def create(self, validated_data):
        sales_goods_items = validated_data.pop('sales_goods_set')
        collection_order_item = validated_data.pop('collection_order', {})
        collection_account_items = collection_order_item.pop('collection_accounts', [])

        validated_data['enable_auto_stock_out'] = self.team.enable_auto_stock_out
        validated_data['creator'] = self.user
        sales_order = super().create(validated_data)

        total_sales_quantity = 0
        total_sales_amount = 0

        # 创建销售商品
        sales_goods_set = []
        for sales_goods_item in sales_goods_items:
            sales_quantity = sales_goods_item['sales_quantity']
            sales_price = sales_goods_item['sales_price']
            total_amount = NP.times(sales_quantity, sales_price)
            sales_goods_set.append(SalesGoods(
                sales_order=sales_order, goods=sales_goods_item['goods'], sales_quantity=sales_quantity,
                sales_price=sales_price, total_amount=total_amount, team=self.team
            ))

            total_sales_quantity = NP.plus(total_sales_quantity, sales_quantity)
            total_sales_amount = NP.plus(total_sales_amount, total_amount)
        else:
            SalesGoods.objects.bulk_create(sales_goods_set)
            total_sales_amount = NP.times(total_sales_amount, sales_order.discount)
            total_sales_amount = NP.plus(total_sales_amount, sales_order.other_amount)
            sales_order.total_quantity = total_sales_quantity
            sales_order.total_amount = total_sales_amount

        total_collection_amount = 0

        # 创建收款单据
        if collection_account_items:
            collection_order_number = CollectionOrder.get_number(team=self.team)
            collection_order_remark = f'销售单据: {sales_order.number}'
            collection_order = CollectionOrder.objects.create(
                number=collection_order_number, client=sales_order.client,
                handler=sales_order.handler, handle_time=sales_order.handle_time,
                remark=collection_order_remark, creator=self.user, team=self.team
            )

            # 创建收款账户
            collection_accounts = []
            for collection_account_item in collection_account_items:
                collection_amount = collection_account_item['collection_amount']
                collection_accounts.append(CollectionAccount(
                    collection_order=collection_order, account=collection_account_item['account'],
                    collection_amount=collection_amount, team=self.team
                ))

                total_collection_amount = NP.plus(total_collection_amount, collection_amount)
            else:
                CollectionAccount.objects.bulk_create(collection_accounts)
                collection_order.total_amount = total_collection_amount
                collection_order.save(update_fields=['total_amount'])
                sales_order.collection_order = collection_order

        sales_order.collection_amount = total_collection_amount
        sales_order.arrears_amount = NP.minus(total_sales_amount, total_collection_amount)
        sales_order.save(update_fields=['total_quantity', 'total_amount', 'collection_amount',
                                        'arrears_amount', 'collection_order'])
        return sales_order


__all__ = [
    'SalesOrderSerializer',
]
