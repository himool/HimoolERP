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
    number = CharField(label='编号')
    name = CharField(label='名称')
    manager_name = CharField(source='manager.name', label='管理员')
    phone = CharField(label='电话')
    address = CharField(label='地址')
    remark = CharField(label='备注')
    order = IntegerField(label='排序')
    is_active = BooleanField(label='激活状态[TRUE/FALSE]')

    class Meta:
        model = Warehouse
        fields = ['number', 'name', 'manager_name', 'phone', 'address', 'remark',
                  'order', 'is_active']


class WarehouseImportSerializer(BaseSerializer):
    number = CharField(label='编号(必填)')
    name = CharField(label='名称(必填)')
    manager_name = CharField(required=False, label='管理员')
    phone = CharField(required=False, label='电话')
    address = CharField(required=False, label='地址')
    remark = CharField(required=False, label='备注')
    order = IntegerField(required=False, label='排序(默认: 100)')
    is_active = BooleanField(required=False, label='激活状态[TRUE/FALSE](默认: TRUE)')

    class Meta:
        model = Warehouse
        fields = ['number', 'name', 'manager_name', 'phone', 'address', 'remark',
                  'order', 'is_active']

    def validate(self, attrs):
        if manager_name := attrs.pop('manager_name', None):
            manager = User.objects.filter(name=manager_name, team=self.team).first()
            if not manager:
                raise ValidationError(f'管理员[{manager_name}]不存在')

            attrs['manager'] = manager

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
    name = CharField(label='名称')
    remark = CharField(label='备注')

    class Meta:
        model = ClientCategory
        fields = ['name', 'remark']


class ClientCategoryImportSerializer(BaseSerializer):
    name = CharField(label='名称(必填)')
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


class ClientExportSerializer(BaseSerializer):
    number = CharField(label='编号')
    name = CharField(label='名称')
    level_display = CharField(source='get_level_display', label='等级')
    category_name = CharField(label='分类')
    contact = CharField(label='联系人')
    phone = CharField(label='手机号')
    email = CharField(label='邮箱')
    address = CharField(label='地址')
    remark = CharField(label='备注')
    order = IntegerField(label='排序')
    is_active = BooleanField(label='激活状态[TRUE/FALSE]')
    initial_arrears_amount = AmountField(label='初期欠款金额')

    class Meta:
        model = Client
        fields = ['number', 'name', 'level_display', 'category_name', 'contact', 'phone',
                  'email', 'address', 'remark', 'order', 'is_active', 'initial_arrears_amount']


class ClientImportSerializer(BaseSerializer):
    number = CharField(label='编号(必填)')
    name = CharField(label='名称(必填)')
    level = CharField(required=False, label='等级[0/1/2/3](默认: 0)')
    category_name = CharField(required=False, label='分类')
    contact = CharField(required=False, label='联系人')
    phone = CharField(required=False, label='手机号')
    email = CharField(required=False, label='邮箱')
    address = CharField(required=False, label='地址')
    remark = CharField(required=False, label='备注')
    order = IntegerField(required=False, label='排序(默认: 100)')
    is_active = BooleanField(required=False, label='激活状态[TRUE/FALSE](默认: TRUE)')
    initial_arrears_amount = AmountField(required=False, label='初期欠款金额(默认: 0)')

    class Meta:
        model = Client
        fields = ['number', 'name', 'level', 'category_name', 'contact', 'phone',
                  'email', 'address', 'remark', 'order', 'is_active', 'initial_arrears_amount']

    def validate(self, attrs):
        if category_name := attrs.pop('category_name', None):
            client_category = ClientCategory.objects.filter(name=category_name, team=self.team).first()
            if not client_category:
                raise ValidationError(f'客户分类[{category_name}]不存在')

            attrs['category'] = client_category

        return super().validate(attrs)


class SupplierCategorySerializer(BaseSerializer):

    class Meta:
        model = SupplierCategory
        read_only_fields = ['id']
        fields = ['name', 'remark', *read_only_fields]

    def validate_name(self, value):
        self.validate_unique({'name': value}, message=f'名称[{value}]已存在')
        return value


class SupplierCategoryExportSerializer(BaseSerializer):
    name = CharField(label='名称')
    remark = CharField(label='备注')

    class Meta:
        model = SupplierCategory
        fields = ['name', 'remark']


class SupplierCategoryImportSerializer(BaseSerializer):
    name = CharField(label='名称(必填)')
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


class SupplierExportSerializer(BaseSerializer):
    number = CharField(label='编号')
    name = CharField(label='名称')
    category_name = CharField(label='分类')
    contact = CharField(label='联系人')
    phone = CharField(label='手机号')
    email = CharField(label='邮箱')
    address = CharField(label='地址')
    bank_account = CharField(label='银行账户')
    bank_name = CharField(label='开户行')
    remark = CharField(label='备注')
    order = IntegerField(label='排序')
    is_active = BooleanField(label='激活状态[TRUE/FALSE]')
    initial_arrears_amount = AmountField(label='初期欠款金额')

    class Meta:
        model = Supplier
        fields = ['number', 'name', 'category_name', 'contact', 'phone', 'email', 'address',
                  'bank_account', 'bank_name', 'remark', 'order', 'is_active', 'initial_arrears_amount']


class SupplierImportSerializer(BaseSerializer):
    number = CharField(label='编号(必填)')
    name = CharField(label='名称(必填)')
    category_name = CharField(required=False, label='分类')
    contact = CharField(required=False, label='联系人')
    phone = CharField(required=False, label='手机号')
    email = CharField(required=False, label='邮箱')
    address = CharField(required=False, label='地址')
    bank_account = CharField(required=False, label='银行账户')
    bank_name = CharField(required=False, label='开户行')
    remark = CharField(required=False, label='备注')
    order = IntegerField(required=False, label='排序(默认: 100)')
    is_active = BooleanField(required=False, label='激活状态[TRUE/FALSE](默认: TRUE)')
    initial_arrears_amount = AmountField(required=False, label='初期欠款金额(默认: 0)')

    class Meta:
        model = Supplier
        fields = ['number', 'name', 'category_name', 'contact', 'phone', 'email', 'address',
                  'bank_account', 'bank_name', 'remark', 'order', 'is_active', 'initial_arrears_amount']

    def validate(self, attrs):
        if category_name := attrs.pop('category_name', None):
            supplier_category = SupplierCategory.objects.filter(name=category_name, team=self.team).first()
            if not supplier_category:
                raise ValidationError(f'供应商分类[{category_name}]不存在')

            attrs['category'] = supplier_category

        return super().validate(attrs)


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


class AccountExportSerializer(BaseSerializer):
    number = CharField(label='编号')
    name = CharField(label='名称')
    type_display = CharField(source='get_type_display', label='账户类型')
    holder = CharField(label='开户人')
    remark = CharField(label='备注')
    order = IntegerField(label='排序')
    is_active = BooleanField(label='激活状态[TRUE/FALSE]')
    initial_balance_amount = AmountField(label='初期余额')

    class Meta:
        model = Account
        fields = ['number', 'name', 'type_display', 'holder', 'remark', 'order', 'is_active',
                  'initial_balance_amount']


class AccountImportSerializer(BaseSerializer):
    number = CharField(label='编号(必填)')
    name = CharField(label='名称(必填)')
    type = CharField(required=False, label='账户类型[cash/alipay/wechat/bank_account/other](默认: cash)')
    holder = CharField(required=False, label='开户人')
    remark = CharField(required=False, label='备注')
    order = IntegerField(required=False, label='排序(默认: 100)')
    is_active = BooleanField(required=False, label='激活状态[TRUE/FALSE](默认: TRUE)')
    initial_balance_amount = AmountField(required=False, label='初期余额(默认: 0)')

    class Meta:
        model = Account
        fields = ['number', 'name', 'type', 'holder', 'remark', 'order', 'is_active',
                  'initial_balance_amount']


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
    'WarehouseSerializer', 'WarehouseExportSerializer', 'WarehouseImportSerializer',
    'ClientCategorySerializer', 'ClientCategoryExportSerializer', 'ClientCategoryImportSerializer',
    'ClientSerializer', 'ClientExportSerializer', 'ClientImportSerializer',
    'SupplierCategorySerializer', 'SupplierCategoryExportSerializer', 'SupplierCategoryImportSerializer',
    'SupplierSerializer', 'SupplierExportSerializer', 'SupplierImportSerializer',
    'AccountSerializer', 'AccountExportSerializer', 'AccountImportSerializer',
    'ChargeItemSerializer', 'ChargeItemExportSerializer', 'ChargeItemImportSerializer',
]
