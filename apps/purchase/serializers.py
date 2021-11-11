from extensions.serializers import *
from extensions.exceptions import *
from apps.purchase.models import *
from apps.finance.models import *
from apps.data.models import *
from apps.goods.models import *
from apps.system.models import *


class PurchaseOrderSerializer(BaseSerializer):
    """采购单据"""

    class PurchaseGoodsSerializer(BaseSerializer):
        """采购商品"""

        goods_number = CharField(source='goods.number', read_only=True, label='商品编号')
        goods_name = CharField(source='goods.name', read_only=True, label='商品名称')
        goods_barcode = CharField(source='goods.barcode', read_only=True, label='商品条码')
        unit_name = CharField(source='goods.unit.name', read_only=True, label='单位名称')

        class Meta:
            model = PurchaseGoods
            read_only_fields = ['id', 'goods_number', 'goods_name', 'goods_barcode', 'total_amount',
                                'return_quantity', 'unit_name']
            fields = ['goods', 'purchase_quantity', 'purchase_price', *read_only_fields]

        def validate_goods(self, instance):
            instance = self.validate_foreign_key(Goods, instance, message='商品不存在')
            if not instance.is_active:
                raise ValidationError(f'商品[{instance.name}]未激活')
            return instance

        def validate_purchase_quantity(self, value):
            if value <= 0:
                raise ValidationError('采购数量小于或等于零')
            return value

        def validate_purchase_price(self, value):
            if value <= 0:
                raise ValidationError('采购单价小于或等于零')
            return value

    class PaymentAccountSerializer(BaseSerializer):
        """付款账户"""

        account_number = CharField(source='account.number', read_only=True, label='账户编号')
        account_name = CharField(source='account.name', read_only=True, label='账户名称')

        class Meta:
            model = PaymentAccount
            read_only_fields = ['id', 'account_number', 'account_name']
            fields = ['account', 'payment_amount', *read_only_fields]

        def validate_account(self, instance):
            instance = self.validate_foreign_key(Account, instance, message='账户不存在')
            if not instance.is_active:
                raise ValidationError(f'账户[{instance.name}]未激活')
            return instance

        def validate_payment_amount(self, value):
            if value <= 0:
                raise ValidationError('付款金额小于或等于零')
            return value

    warehouse_number = CharField(source='warehouse.number', read_only=True, label='仓库编号')
    warehouse_name = CharField(source='warehouse.name', read_only=True, label='仓库名称')
    supplier_number = CharField(source='supplier.number', read_only=True, label='供应商编号')
    supplier_name = CharField(source='supplier.name', read_only=True, label='供应商名称')
    handler_name = CharField(source='handler.name', read_only=True, label='经手人名称')
    creator_name = CharField(source='creator.name', read_only=True, label='创建人名称')
    purchase_goods_items = PurchaseGoodsSerializer(source='purchase_goods_set',  many=True, label='采购商品')
    payment_account_items = PaymentAccountSerializer(source='payment_order.payment_accounts',
                                                     required=False, many=True, label='付款账户')

    class Meta:
        model = PurchaseOrder
        read_only_fields = ['id', 'warehouse_number', 'warehouse_name', 'supplier_number', 'supplier_name',
                            'handler_name', 'total_amount', 'total_quantity', 'payment_amount', 'arrears_amount',
                            'is_void', 'enable_auto_stock_in', 'creator_name', 'create_time']
        fields = ['number', 'warehouse', 'supplier', 'handler', 'handle_time', 'other_amount', 'remark',
                  'purchase_goods_items', 'payment_account_items', *read_only_fields]

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

    def validate_supplier(self, instance):
        instance = self.validate_foreign_key(Supplier, instance, message='供应商不存在')
        if not instance.is_active:
            raise ValidationError(f'供应商[{instance.name}]未激活')
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
        purchase_goods_items = validated_data.pop('purchase_goods_set')
        payment_order_item = validated_data.pop('payment_order', {})
        payment_account_items = payment_order_item.pop('payment_accounts', [])
        
        validated_data['enable_auto_stock_in'] = self.team.enable_auto_stock_in
        validated_data['creator'] = self.user
        purchase_order = super().create(validated_data)

        total_purchase_quantity = 0
        total_purchase_amount = 0

        # 创建采购商品
        purchase_goods_set = []
        for purchase_goods_item in purchase_goods_items:
            purchase_quantity = purchase_goods_item['purchase_quantity']
            purchase_price = purchase_goods_item['purchase_price']
            total_amount = NP.times(purchase_quantity, purchase_price)
            purchase_goods_set.append(PurchaseGoods(
                purchase_order=purchase_order, goods=purchase_goods_item['goods'],
                purchase_quantity=purchase_quantity, purchase_price=purchase_price,
                total_amount=total_amount, team=self.team
            ))

            total_purchase_quantity = NP.plus(total_purchase_quantity, purchase_quantity)
            total_purchase_amount = NP.plus(total_purchase_amount, total_amount)
        else:
            PurchaseGoods.objects.bulk_create(purchase_goods_set)
            total_purchase_amount = NP.plus(total_purchase_amount, purchase_order.other_amount)
            purchase_order.total_quantity = total_purchase_quantity
            purchase_order.total_amount = total_purchase_amount

        total_payment_amount = 0

        # 创建付款单据
        if payment_account_items:
            payment_order_number = PaymentOrder.get_number(team=self.team)
            payment_order_remark = f'采购单据: {purchase_order.number}'
            payment_order = PaymentOrder.objects.create(
                number=payment_order_number, supplier=purchase_order.supplier,
                handler=purchase_order.handler, handle_time=purchase_order.handle_time,
                remark=payment_order_remark, creator=self.user, team=self.team
            )

            # 创建付款账户
            payment_accounts = []
            for payment_account_item in payment_account_items:
                payment_amount = payment_account_item['payment_amount']
                payment_accounts.append(PaymentAccount(
                    payment_order=payment_order, account=payment_account_item['account'],
                    payment_amount=payment_amount, team=self.team
                ))

                total_payment_amount = NP.plus(total_payment_amount, payment_amount)
            else:
                PaymentAccount.objects.bulk_create(payment_accounts)
                payment_order.total_amount = total_payment_amount
                payment_order.save(update_fields=['total_amount'])
                purchase_order.payment_order = payment_order

        purchase_order.payment_amount = total_payment_amount
        purchase_order.arrears_amount = NP.minus(total_purchase_amount, total_payment_amount)
        purchase_order.save(update_fields=['total_quantity', 'total_amount', 'payment_amount',
                                           'arrears_amount', 'payment_order'])
        return purchase_order


__all__ = [
    'PurchaseOrderSerializer',
]
