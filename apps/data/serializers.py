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
        fields = ['number', 'name', 'manager', 'phone', 'address', 'remark', 'is_active',
                  *read_only_fields]

    def validate_number(self, value):
        self.validate_unique({'number': value}, message=f'编号[{value}]已存在')
        return value

    def validate_name(self, value):
        self.validate_unique({'name': value}, message=f'名称[{value}]已存在')
        return value

    def validate_manager(self, instance):
        instance = self.validate_foreign_key(User, instance, message='管理员不存在')
        if instance and not instance.is_active:
            raise ValidationError(f'管理员[{instance.name}]未激活')
        return instance


class WarehouseImportExportSerializer(BaseSerializer):
    number = CharField(label='仓库编号(必填唯一)', error_messages={
        'invalid': '仓库编号 数据无效, 只支持数字, 文本格式, 不支持公式, xx等其他格式',
        'required': '仓库编号 未填写',
        'blank': '仓库编号 未填写',
        'max_length': '仓库编号 超出最大长度',
    })
    name = CharField(label='仓库名称(必填唯一)', error_messages={
        'invalid': '仓库名称 数据无效, 只支持数字, 文本格式, 不支持公式, xx等其他格式',
        'required': '仓库名称 未填写',
        'blank': '仓库名称 未填写',
        'max_length': '仓库名称 超出最大长度',
    })
    manager = CharField(source='manager.name', required=False, label='管理员', error_messages={
        'invalid': '管理员 数据无效, 只支持数字, 文本格式, 不支持公式, xx等其他格式',
    })
    phone = CharField(required=False, label='电话', error_messages={
        'invalid': '电话 数据无效, 只支持数字, 文本格式, 不支持公式, xx等其他格式',
        'max_length': '电话 超出最大长度',
    })
    address = CharField(required=False, label='地址', error_messages={
        'invalid': '地址 数据无效, 只支持数字, 文本格式, 不支持公式, xx等其他格式',
        'max_length': '地址 超出最大长度',
    })
    remark = CharField(required=False, label='备注', error_messages={
        'invalid': '备注 数据无效, 只支持数字, 文本格式, 不支持公式, xx等其他格式',
        'max_length': '备注 超出最大长度',
    })
    is_active = BooleanField(required=False, label='激活状态[TRUE/FALSE](默认: TRUE)', error_messages={
        'invalid': '激活状态 数据无效, 只支持数字, 文本格式, 不支持公式, xx等其他格式',
    })

    class Meta:
        model = Warehouse
        fields = ['number', 'name', 'manager', 'phone', 'address', 'remark',
                  'is_active']


class ClientSerializer(BaseSerializer):
    level_display = CharField(source='get_level_display', read_only=True, label='等级')

    class Meta:
        model = Client
        read_only_fields = ['id', 'level_display']
        fields = ['number', 'name', 'level', 'contact', 'phone', 'email', 'address',
                  'remark', 'is_active', 'initial_arrears_amount', *read_only_fields]

    def validate_number(self, value):
        self.validate_unique({'number': value}, message=f'编号[{value}]已存在')
        return value

    def validate_name(self, value):
        self.validate_unique({'name': value}, message=f'名称[{value}]已存在')
        return value

    def create(self, validated_data):
        validated_data['arrears_amount'] = validated_data.get('initial_arrears_amount', 0)
        validated_data['has_arrears'] = validated_data['arrears_amount'] > 0
        return super().create(validated_data)

    def update(self, instance, validated_data):
        initial_arrears_amount = validated_data.get('initial_arrears_amount')
        if initial_arrears_amount is not None and instance.initial_arrears_amount != initial_arrears_amount:
            arrears_amount = NP.minus(instance.arrears_amount, instance.initial_arrears_amount)
            validated_data['arrears_amount'] = NP.plus(arrears_amount, validated_data['initial_arrears_amount'])
            validated_data['has_arrears'] = validated_data['arrears_amount'] > 0

        return super().update(instance, validated_data)


class ClientImportExportSerializer(BaseSerializer):
    number = CharField(label='客户编号(必填唯一)', error_messages={
        'invalid': '客户编号 数据无效, 只支持数字, 文本格式, 不支持公式, xx等其他格式',
        'required': '客户编号 未填写',
        'blank': '客户编号 未填写',
        'max_length': '客户编号 超出最大长度',
    })
    name = CharField(label='客户名称(必填唯一)', error_messages={
        'invalid': '客户名称 数据无效, 只支持数字, 文本格式, 不支持公式, xx等其他格式',
        'required': '客户名称 未填写',
        'blank': '客户名称 未填写',
        'max_length': '客户名称 超出最大长度',
    })
    level = CharField(required=False, label='等级[0/1/2/3](默认: 0)', error_messages={
        'invalid': '等级 数据无效, 只支持数字, 文本格式, 不支持公式, xx等其他格式',
    })
    contact = CharField(required=False, label='联系人', error_messages={
        'invalid': '联系人 数据无效, 只支持数字, 文本格式, 不支持公式, xx等其他格式',
        'max_length': '联系人 超出最大长度',
    })
    phone = CharField(required=False, label='手机号', error_messages={
        'invalid': '手机号 数据无效, 只支持数字, 文本格式, 不支持公式, xx等其他格式',
        'max_length': '手机号 超出最大长度',
    })
    email = CharField(required=False, label='邮箱', error_messages={
        'invalid': '邮箱 数据无效, 只支持数字, 文本格式, 不支持公式, xx等其他格式',
        'max_length': '邮箱 超出最大长度',
    })
    address = CharField(required=False, label='地址', error_messages={
        'invalid': '地址 数据无效, 只支持数字, 文本格式, 不支持公式, xx等其他格式',
        'max_length': '地址 超出最大长度',
    })
    remark = CharField(required=False, label='备注', error_messages={
        'invalid': '备注 数据无效, 只支持数字, 文本格式, 不支持公式, xx等其他格式',
        'max_length': '备注 超出最大长度',
    })
    is_active = BooleanField(required=False, label='激活状态[TRUE/FALSE](默认: TRUE)', error_messages={
        'invalid': '激活状态 数据无效, 只支持数字, 文本格式, 不支持公式, xx等其他格式',
    })

    class Meta:
        model = Client
        fields = ['number', 'name', 'level', 'contact', 'phone', 'email', 'address', 'remark',
                  'is_active']


class SupplierSerializer(BaseSerializer):

    class Meta:
        model = Supplier
        read_only_fields = ['id']
        fields = ['number', 'name', 'contact', 'phone', 'email', 'address', 'bank_account',
                  'bank_name', 'remark', 'is_active', 'initial_arrears_amount', *read_only_fields]

    def validate_number(self, value):
        self.validate_unique({'number': value}, message=f'编号[{value}]已存在')
        return value

    def validate_name(self, value):
        self.validate_unique({'name': value}, message=f'名称[{value}]已存在')
        return value

    def create(self, validated_data):
        validated_data['arrears_amount'] = validated_data.get('initial_arrears_amount', 0)
        validated_data['has_arrears'] = validated_data['arrears_amount'] > 0
        return super().create(validated_data)

    def update(self, instance, validated_data):
        initial_arrears_amount = validated_data.get('initial_arrears_amount')
        if initial_arrears_amount is not None and instance.initial_arrears_amount != initial_arrears_amount:
            arrears_amount = NP.minus(instance.arrears_amount, instance.initial_arrears_amount)
            validated_data['arrears_amount'] = NP.plus(arrears_amount, validated_data['initial_arrears_amount'])
            validated_data['has_arrears'] = validated_data['arrears_amount'] > 0

        return super().update(instance, validated_data)


class SupplierImportExportSerializer(BaseSerializer):
    number = CharField(label='供应商编号(必填唯一)', error_messages={
        'invalid': '供应商编号 数据无效, 只支持数字, 文本格式, 不支持公式, xx等其他格式',
        'required': '供应商编号 未填写',
        'blank': '供应商编号 未填写',
        'max_length': '供应商编号 超出最大长度',
    })
    name = CharField(label='供应商名称(必填唯一)', error_messages={
        'invalid': '供应商名称 数据无效, 只支持数字, 文本格式, 不支持公式, xx等其他格式',
        'required': '供应商名称 未填写',
        'blank': '供应商名称 未填写',
        'max_length': '供应商名称 超出最大长度',
    })
    contact = CharField(required=False, label='联系人', error_messages={
        'invalid': '联系人 数据无效, 只支持数字, 文本格式, 不支持公式, xx等其他格式',
        'max_length': '联系人 超出最大长度',
    })
    phone = CharField(required=False, label='手机号', error_messages={
        'invalid': '手机号 数据无效, 只支持数字, 文本格式, 不支持公式, xx等其他格式',
        'max_length': '手机号 超出最大长度',
    })
    email = CharField(required=False, label='邮箱', error_messages={
        'invalid': '邮箱 数据无效, 只支持数字, 文本格式, 不支持公式, xx等其他格式',
        'max_length': '邮箱 超出最大长度',
    })
    address = CharField(required=False, label='地址', error_messages={
        'invalid': '地址 数据无效, 只支持数字, 文本格式, 不支持公式, xx等其他格式',
        'max_length': '地址 超出最大长度',
    })
    bank_account = CharField(required=False, label='银行账户', error_messages={
        'invalid': '银行账户 数据无效, 只支持数字, 文本格式, 不支持公式, xx等其他格式',
        'max_length': '银行账户 超出最大长度',
    })
    bank_name = CharField(required=False, label='开户行', error_messages={
        'invalid': '开户行 数据无效, 只支持数字, 文本格式, 不支持公式, xx等其他格式',
        'max_length': '开户行 超出最大长度',
    })
    remark = CharField(required=False, label='备注', error_messages={
        'invalid': '备注 数据无效, 只支持数字, 文本格式, 不支持公式, xx等其他格式',
        'max_length': '备注 超出最大长度',
    })
    is_active = BooleanField(required=False, label='激活状态[TRUE/FALSE](默认: TRUE)', error_messages={
        'invalid': '激活状态 数据无效, 只支持数字, 文本格式, 不支持公式, xx等其他格式',
    })

    class Meta:
        model = Supplier
        fields = ['number', 'name', 'contact', 'phone', 'email', 'address', 'bank_account',
                  'bank_name', 'remark', 'is_active']


class AccountSerializer(BaseSerializer):
    type_display = CharField(source='get_type_display', read_only=True, label='账户类型')

    class Meta:
        model = Account
        read_only_fields = ['id', 'type_display', 'balance_amount', 'has_balance']
        fields = ['number', 'name', 'type', 'holder', 'card_number', 'remark', 'is_active',
                  'initial_balance_amount', *read_only_fields]

    def validate_number(self, value):
        self.validate_unique({'number': value}, message=f'编号[{value}]已存在')
        return value

    def validate_name(self, value):
        self.validate_unique({'name': value}, message=f'名称[{value}]已存在')
        return value

    def create(self, validated_data):
        validated_data['balance_amount'] = validated_data.get('initial_balance_amount', 0)
        validated_data['has_balance'] = validated_data['balance_amount'] > 0
        return super().create(validated_data)

    def update(self, instance, validated_data):
        initial_balance_amount = validated_data.get('initial_arrears_amount')
        if initial_balance_amount is not None and instance.initial_balance_amount != initial_balance_amount:
            balance_amount = NP.minus(instance.balance_amount, instance.initial_balance_amount)
            validated_data['balance_amount'] = NP.plus(balance_amount, validated_data['initial_balance_amount'])
            validated_data['has_balance'] = validated_data['balance_amount'] > 0

        return super().update(instance, validated_data)


class AccountImportExportSerializer(BaseSerializer):
    number = CharField(label='账户编号(必填唯一)', error_messages={
        'invalid': '账户编号 数据无效, 只支持数字, 文本格式, 不支持公式, xx等其他格式',
        'required': '账户编号 未填写',
        'blank': '账户编号 未填写',
        'max_length': '账户编号 超出最大长度',
    })
    name = CharField(label='账户名称(必填唯一)', error_messages={
        'invalid': '账户名称 数据无效, 只支持数字, 文本格式, 不支持公式, xx等其他格式',
        'required': '账户名称 未填写',
        'blank': '账户名称 未填写',
        'max_length': '账户名称 超出最大长度',
    })
    type = CharField(required=False, label='账户类型[cash/alipay/wechat/bank_account/other](默认: cash)', error_messages={
        'invalid': '账户类型 数据无效, 只支持数字, 文本格式, 不支持公式, xx等其他格式',
        'max_length': '账户类型 超出最大长度',
    })
    holder = CharField(required=False, label='开户人', error_messages={
        'invalid': '开户人 数据无效, 只支持数字, 文本格式, 不支持公式, xx等其他格式',
        'max_length': '开户人 超出最大长度',
    })
    card_number = CharField(required=False, label='开户账号', error_messages={
        'invalid': '开户账号 数据无效, 只支持数字, 文本格式, 不支持公式, xx等其他格式',
        'max_length': '开户账号 超出最大长度',
    })
    remark = CharField(required=False, label='备注', error_messages={
        'invalid': '备注 数据无效, 只支持数字, 文本格式, 不支持公式, xx等其他格式',
        'max_length': '备注 超出最大长度',
    })
    is_active = BooleanField(required=False, label='激活状态[TRUE/FALSE](默认: TRUE)', error_messages={
        'invalid': '激活状态 数据无效, 只支持数字, 文本格式, 不支持公式, xx等其他格式',
    })

    class Meta:
        model = Account
        fields = ['number', 'name', 'type', 'holder', 'card_number', 'remark', 'is_active']


class ChargeItemSerializer(BaseSerializer):
    type_display = CharField(source='get_type_display', read_only=True, label='收支类型')

    class Meta:
        model = ChargeItem
        read_only_fields = ['id', 'type_display']
        fields = ['name', 'type', 'remark', *read_only_fields]

    def validate_name(self, value):
        self.validate_unique({'name': value}, message=f'名称[{value}]已存在')
        return value


class ChargeItemImportExportSerializer(BaseSerializer):
    name = CharField(label='收支项目(必填唯一)', error_messages={
        'invalid': '收支项目 数据无效, 只支持数字, 文本格式, 不支持公式, xx等其他格式',
        'required': '收支项目 未填写',
        'blank': '收支项目 未填写',
        'max_length': '收支项目 超出最大长度',
    })
    type = CharField(label='收支类型[income/expenditure](必填)', error_messages={
        'invalid': '收支类型 数据无效, 只支持数字, 文本格式, 不支持公式, xx等其他格式',
        'required': '收支类型 未填写',
        'blank': '收支类型 未填写',
        'max_length': '收支类型 超出最大长度',
    })
    remark = CharField(required=False, label='备注', error_messages={
        'invalid': '备注 数据无效, 只支持数字, 文本格式, 不支持公式, xx等其他格式',
        'max_length': '备注 超出最大长度',
    })

    class Meta:
        model = ChargeItem
        fields = ['name', 'type', 'remark']


__all__ = [
    'WarehouseSerializer', 'WarehouseImportExportSerializer',
    'ClientSerializer', 'ClientImportExportSerializer',
    'SupplierSerializer', 'SupplierImportExportSerializer',
    'AccountSerializer', 'AccountImportExportSerializer',
    'ChargeItemSerializer', 'ChargeItemImportExportSerializer',
]
