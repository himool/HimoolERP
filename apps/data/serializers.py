from extensions.common.base import *
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
        instance = self.validate_foreign_key(User, instance, message='管理员不存在')
        if not instance.is_active:
            raise ValidationError(f'管理员[{instance.name}]未激活')
        return instance


class WarehouseExportSerializer(BaseSerializer):
    number = CharField(label='仓库编号')
    name = CharField(label='仓库名称')
    manager_username = CharField(source='manager.username', label='管理员用户名')
    manager_name = CharField(source='manager.name', label='管理员名称')
    phone = CharField(label='电话')
    address = CharField(label='地址')
    remark = CharField(label='备注')
    order = IntegerField(label='排序')
    is_active = BooleanField(label='激活状态[TRUE/FALSE]')

    class Meta:
        model = Warehouse
        fields = ['number', 'name', 'manager_username', 'manager_name', 'phone', 'address',
                  'remark', 'order', 'is_active']


class WarehouseImportSerializer(BaseSerializer):
    number = CharField(label='仓库编号(必填)')
    name = CharField(label='仓库名称(必填)')
    manager_username = CharField(required=False, label='管理员用户名')
    phone = CharField(required=False, label='电话')
    address = CharField(required=False, label='地址')
    remark = CharField(required=False, label='备注')
    order = IntegerField(required=False, label='排序(默认: 100)')
    is_active = BooleanField(required=False, label='激活状态[TRUE/FALSE](默认: TRUE)')

    class Meta:
        model = Warehouse
        fields = ['number', 'name', 'manager_username', 'phone', 'address', 'remark',
                  'order', 'is_active']

    def validate(self, attrs):
        if manager_username := attrs.pop('manager_username', None):
            manager = User.objects.filter(username=manager_username, team=self.team).first()
            if not manager:
                raise ValidationError(f'管理员[{manager_username}]不存在')

            attrs['manager'] = manager
        else:
            attrs['manager'] = None

        return super().validate(attrs)


class ClientCategorySerializer(BaseSerializer):

    class Meta:
        model = ClientCategory
        read_only_fields = ['id']
        fields = ['name', 'remark', *read_only_fields]

    def validate_name(self, value):
        self.validate_unique({'name': value}, message=f'名称[{value}]已存在')
        return value


class ClientCategoryExportSerializer(BaseSerializer):
    name = CharField(label='客户分类名称')
    remark = CharField(label='备注')

    class Meta:
        model = ClientCategory
        fields = ['name', 'remark']


class ClientCategoryImportSerializer(BaseSerializer):
    name = CharField(label='客户分类名称(必填)')
    remark = CharField(required=False, label='备注')

    class Meta:
        model = ClientCategory
        fields = ['name', 'remark']


class ClientSerializer(BaseSerializer):
    level_display = CharField(source='get_level_display', read_only=True, label='等级')
    category_name = CharField(source='category.name', read_only=True, label='分类名称')

    class Meta:
        model = Client
        read_only_fields = ['id', 'level_display', 'category_name', 'arrears_amount', 'has_arrears']
        fields = ['number', 'name', 'level', 'category', 'contact', 'phone', 'email', 'address',
                  'remark', 'order', 'is_active', 'initial_arrears_amount', *read_only_fields]

    def validate_number(self, value):
        self.validate_unique({'number': value}, message=f'编号[{value}]已存在')
        return value

    def validate_name(self, value):
        self.validate_unique({'name': value}, message=f'名称[{value}]已存在')
        return value

    def validate_category(self, instance):
        instance = self.validate_foreign_key(ClientCategory, instance, message='客户分类不存在')
        return instance

    def create(self, validated_data):
        validated_data['arrears_amount'] = validated_data.get('initial_arrears_amount', 0)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        initial_arrears_amount = validated_data.get('initial_arrears_amount')
        if initial_arrears_amount is not None and instance.initial_arrears_amount != initial_arrears_amount:
            arrears_amount = NP.minus(instance.arrears_amount, instance.initial_arrears_amount)
            validated_data['arrears_amount'] = NP.plus(arrears_amount, validated_data['initial_arrears_amount'])

        return super().update(instance, validated_data)


class SupplierCategorySerializer(BaseSerializer):

    class Meta:
        model = SupplierCategory
        read_only_fields = ['id']
        fields = ['name', 'remark', *read_only_fields]

    def validate_name(self, value):
        self.validate_unique({'name': value}, message=f'名称[{value}]已存在')
        return value


class SupplierCategoryExportSerializer(BaseSerializer):
    name = CharField(label='供应商分类名称')
    remark = CharField(label='备注')

    class Meta:
        model = SupplierCategory
        fields = ['name', 'remark']


class SupplierCategoryImportSerializer(BaseSerializer):
    name = CharField(label='供应商分类名称(必填)')
    remark = CharField(required=False, label='备注')

    class Meta:
        model = SupplierCategory
        fields = ['name', 'remark']


class SupplierSerializer(BaseSerializer):
    category_name = CharField(source='category.name', read_only=True, label='分类名称')

    class Meta:
        model = Supplier
        read_only_fields = ['id', 'category_name', 'arrears_amount', 'has_arrears']
        fields = ['number', 'name', 'category', 'contact', 'phone', 'email', 'address', 'bank_account',
                  'bank_name', 'remark', 'order', 'is_active', 'initial_arrears_amount', *read_only_fields]

    def validate_number(self, value):
        self.validate_unique({'number': value}, message=f'编号[{value}]已存在')
        return value

    def validate_name(self, value):
        self.validate_unique({'name': value}, message=f'名称[{value}]已存在')
        return value

    def validate_category(self, instance):
        instance = self.validate_foreign_key(SupplierCategory, instance, message='供应商分类不存在')
        return instance

    def create(self, validated_data):
        validated_data['arrears_amount'] = validated_data.get('initial_arrears_amount', 0)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        initial_arrears_amount = validated_data.get('initial_arrears_amount')
        if initial_arrears_amount is not None and instance.initial_arrears_amount != initial_arrears_amount:
            arrears_amount = NP.minus(instance.arrears_amount, instance.initial_arrears_amount)
            validated_data['arrears_amount'] = NP.plus(arrears_amount, validated_data['initial_arrears_amount'])

        return super().update(instance, validated_data)


class AccountSerializer(BaseSerializer):
    type_display = CharField(source='get_type_display', read_only=True, label='账户类型')

    class Meta:
        model = Account
        read_only_fields = ['id', 'type_display', 'balance_amount', 'has_balance']
        fields = ['number', 'name', 'type', 'holder', 'remark', 'order', 'is_active',
                  'initial_balance_amount', *read_only_fields]

    def validate_number(self, value):
        self.validate_unique({'number': value}, message=f'编号[{value}]已存在')
        return value

    def validate_name(self, value):
        self.validate_unique({'name': value}, message=f'名称[{value}]已存在')
        return value

    def create(self, validated_data):
        validated_data['balance_amount'] = validated_data.get('initial_balance_amount', 0)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        initial_balance_amount = validated_data.get('initial_arrears_amount')
        if initial_balance_amount is not None and instance.initial_balance_amount != initial_balance_amount:
            balance_amount = NP.minus(instance.balance_amount, instance.initial_balance_amount)
            validated_data['balance_amount'] = NP.plus(balance_amount, validated_data['initial_balance_amount'])

        return super().update(instance, validated_data)


class ChargeItemSerializer(BaseSerializer):
    type_display = CharField(source='get_type_display', read_only=True, label='收支类型')

    class Meta:
        model = ChargeItem
        read_only_fields = ['id', 'type_display']
        fields = ['name', 'type', 'remark', *read_only_fields]

    def validate_name(self, value):
        self.validate_unique({'name': value}, message=f'名称[{value}]已存在')
        return value


class ChargeItemExportSerializer(BaseSerializer):
    name = CharField(label='收支项目名称')
    type_display = CharField(source='get_type_display', label='收支项目名称')
    remark = CharField(label='备注')

    class Meta:
        model = ChargeItem
        fields = ['name', 'remark']


class ChargeItemImportSerializer(BaseSerializer):
    name = CharField(label='收支项目名称(必填)')
    type = CharField(label='收支类型[income/expenditure](必填)')
    remark = CharField(required=False, label='备注')

    class Meta:
        model = ChargeItem
        fields = ['name', 'type', 'remark']


__all__ = [
    'WarehouseSerializer',
    'ClientCategorySerializer', 'ClientCategoryExportSerializer', 'ClientCategoryImportSerializer',
    'ClientSerializer',
    'SupplierCategorySerializer', 'SupplierCategoryExportSerializer', 'SupplierCategoryImportSerializer',
    'SupplierSerializer',
    'AccountSerializer',
    'ChargeItemSerializer', 'ChargeItemExportSerializer', 'ChargeItemImportSerializer',
]
