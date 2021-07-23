from .models import Supplier, PurchaseOrder, ChangeRecord, PaymentRecord
from rest_framework import serializers


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['id', 'name', 'manager', 'phone', 'address', 'email', 'bank_account', 'bank_name',
                  'order', 'status', 'address', 'url', 'default_discount', 'remark', 'update_date']
        read_only_fields = ['id', 'update_date']

    def validate(self, data):
        if not data.get('name') or data.get('default_discount') is None:
            raise serializers.ValidationError
        return data


class PurchaseOrderSerializer(serializers.ModelSerializer):
    goods_set = serializers.SerializerMethodField('get_goods_set')

    class Meta:
        model = PurchaseOrder
        read_only_fields = ['id', 'supplier_name', 'warehouse_name', 'warehouse_address', 'account_name',
                            'contacts_name', 'contacts_phone', 'is_done', 'goods_set', 'total_amount']
        fields = ['supplier', 'warehouse', 'account', 'contacts', 'amount', 'date', 'remark',
                  'is_return', 'purchase_order', *read_only_fields]

    def validate(self, data):
        if not data.get('supplier') or not data.get('warehouse') or not data.get('account'):
            raise serializers.ValidationError

        if not data.get('contacts') or data.get('amount') is None or not data.get('date'):
            raise serializers.ValidationError

        # goods_set
        goods_set = self.context['request'].data.get('goods_set', [])
        if not goods_set:
            raise serializers.ValidationError

        for item in goods_set:
            if item.get('id') is None or item.get('purchase_price') is None:
                raise serializers.ValidationError

            quantity = item.get('quantity')
            discount = item.get('discount')
            if not quantity or quantity <= 0 or not discount or discount <= 0:
                raise serializers.ValidationError

        # 退货单
        if data.get('is_return', False) and not data.get('purchase_order'):
            raise serializers.ValidationError

        return data

    def get_goods_set(self, obj):
        return obj.goods_set.all().values('id', 'code', 'name', 'specification', 'unit', 'purchase_price', 'quantity',
                                          'discount', 'discount_price', 'amount', 'discount_amount')


class PurchasePaymentRecordSerializer(serializers.ModelSerializer):
    supplier_name = serializers.SerializerMethodField('get_supplier_name')

    class Meta:
        model = PaymentRecord
        read_only_fields = ['purchase_order', 'date', 'amount',  'remark', 'supplier_name']
        fields = [*read_only_fields]

    def get_supplier_name(self, obj):
        return obj.purchase_order.supplier_name


class ChangeRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChangeRecord
        fields = ['create_datetime', 'goods_code', 'goods_name', 'specification', 'unit', 'change_method',
                  'before_change', 'after_change', 'operator', 'relation_order']
        read_only_fields = fields
