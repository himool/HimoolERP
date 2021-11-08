from extensions.serializers import *
from extensions.exceptions import *
from apps.data.models import *
from apps.system.models import *


class WarehouseSerializer(BaseSerializer):
    manager_name = CharField(source='manager.name', read_only=True, label='管理员名称')

    class Meta:
        model = Warehouse
        read_only_fields = ['id', 'manager_name']
        fields = ['number', 'name', 'manager', 'phone', 'address', 'remark', 'order', 'is_active',
                  'is_locked', *read_only_fields]

    def validate_number(self, value):
        self.validate_unique({'number': value}, message=f'编号[{value}]已存在')
        return value

    def validate_name(self, value):
        self.validate_unique({'name': value}, message=f'名称[{value}]已存在')
        return value

    def validate_manager(self, instance):
        instance = self.validate_foreign_key(User, instance)
        if not instance.is_active:
            raise ValidationError(f'管理员[{instance.name}]未激活')
        return instance


class ClientSerializer(BaseSerializer):
    category_name = CharField(source='category.name', read_only=True, label='分类名称')

    class Meta:
        model = Client
        read_only_fields = ['id', 'category_name', 'arrears_amount']
        fields = ['number', 'name', 'category', 'contact', 'phone', 'email', 'address', 'remark',
                  'order', 'is_active', 'initial_arrears_amount', *read_only_fields]

    def validate_number(self, value):
        self.validate_unique({'number': value}, message=f'编号[{value}]已存在')
        return value

    def validate_name(self, value):
        self.validate_unique({'name': value}, message=f'名称[{value}]已存在')
        return value

    def validate_category(self, instance):
        instance = self.validate_foreign_key(ClientCategory, instance)
        return instance

    def create(self, validated_data):
        validated_data['arrears_amount'] = validated_data['initial_arrears_amount']
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if instance.initial_arrears_amount != validated_data['initial_arrears_amount']:
            arrears_amount = NP.minus(instance.arrears_amount, instance.initial_arrears_amount)
            validated_data['arrears_amount'] = NP.plus(arrears_amount, validated_data['initial_arrears_amount'])

        return super().update(instance, validated_data)


class SupplierSerializer(BaseSerializer):
    category_name = CharField(source='category.name', read_only=True, label='分类名称')

    class Meta:
        model = Supplier
        read_only_fields = ['id', 'category_name', 'arrears_amount']
        fields = ['number', 'name', 'category', 'contact', 'phone', 'email', 'address', 'bank_account',
                  'bank_name', 'remark', 'order', 'is_active', 'initial_arrears_amount', *read_only_fields]

    def validate_number(self, value):
        self.validate_unique({'number': value}, message=f'编号[{value}]已存在')
        return value

    def validate_name(self, value):
        self.validate_unique({'name': value}, message=f'名称[{value}]已存在')
        return value

    def validate_category(self, instance):
        instance = self.validate_foreign_key(SupplierCategory, instance)
        return instance

    def create(self, validated_data):
        validated_data['arrears_amount'] = validated_data['initial_arrears_amount']
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if instance.initial_arrears_amount != validated_data['initial_arrears_amount']:
            arrears_amount = NP.minus(instance.arrears_amount, instance.initial_arrears_amount)
            validated_data['arrears_amount'] = NP.plus(arrears_amount, validated_data['initial_arrears_amount'])

        return super().update(instance, validated_data)


class AccountSerializer(BaseSerializer):

    class Meta:
        model = Account
        read_only_fields = ['id', 'balance_amount']
        fields = ['number', 'name', 'type', 'holder', 'remark', 'order', 'is_active',
                  'initial_balance_amount', *read_only_fields]

    def validate_number(self, value):
        self.validate_unique({'number': value}, message=f'编号[{value}]已存在')
        return value

    def validate_name(self, value):
        self.validate_unique({'name': value}, message=f'名称[{value}]已存在')
        return value

    def create(self, validated_data):
        validated_data['balance_amount'] = validated_data['initial_balance_amount']
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if instance.initial_balance_amount != validated_data['initial_balance_amount']:
            balance_amount = NP.minus(instance.balance_amount, instance.initial_balance_amount)
            validated_data['balance_amount'] = NP.plus(balance_amount, validated_data['initial_balance_amount'])

        return super().update(instance, validated_data)


class ChargeItemSerializer(BaseSerializer):

    class Meta:
        model = ChargeItem
        read_only_fields = ['id']
        fields = ['name', 'type', 'remark', *read_only_fields]

    def validate_name(self, value):
        self.validate_unique({'name': value}, message=f'名称[{value}]已存在')
        return value


class ClientCategorySerializer(BaseSerializer):

    class Meta:
        model = ClientCategory
        read_only_fields = ['id']
        fields = ['name', 'remark', *read_only_fields]

    def validate_name(self, value):
        self.validate_unique({'name': value}, message=f'名称[{value}]已存在')
        return value


class SupplierCategorySerializer(BaseSerializer):

    class Meta:
        model = SupplierCategory
        read_only_fields = ['id']
        fields = ['name', 'remark', *read_only_fields]

    def validate_name(self, value):
        self.validate_unique({'name': value}, message=f'名称[{value}]已存在')
        return value


class GoodsCategorySerializer(BaseSerializer):

    class Meta:
        model = GoodsCategory
        read_only_fields = ['id']
        fields = ['name', 'remark', *read_only_fields]

    def validate_name(self, value):
        self.validate_unique({'name': value}, message=f'名称[{value}]已存在')
        return value


class GoodsUnitSerializer(BaseSerializer):

    class Meta:
        model = GoodsUnit
        read_only_fields = ['id']
        fields = ['name', 'remark', *read_only_fields]

    def validate_name(self, value):
        self.validate_unique({'name': value}, message=f'名称[{value}]已存在')
        return value


__all__ = [
    'WarehouseSerializer', 'ClientSerializer', 'SupplierSerializer', 'AccountSerializer',
    'ChargeItemSerializer', 'ClientCategorySerializer', 'SupplierCategorySerializer',
    'GoodsCategorySerializer', 'GoodsUnitSerializer',
]
