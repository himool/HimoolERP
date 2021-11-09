from extensions.models import *


class Warehouse(Model):
    """仓库"""

    number = CharField(max_length=32, verbose_name='编号')
    name = CharField(max_length=64, verbose_name='名称')
    manager = ForeignKey('system.User', on_delete=CASCADE, null=True,
                         related_name='warehouses', verbose_name='管理员')
    phone = CharField(max_length=32, null=True, blank=True, verbose_name='电话')
    address = CharField(max_length=256, null=True, blank=True, verbose_name='地址')
    remark = CharField(max_length=256, null=True, blank=True, verbose_name='备注')
    order = IntegerField(default=100, verbose_name='顺序')
    is_active = BooleanField(default=True, verbose_name='激活状态')
    is_locked = BooleanField(default=True, verbose_name='锁定状态')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='warehouses')

    class Meta:
        unique_together = [('number', 'team'), ('name', 'team')]


class Client(Model):
    """客户"""
    
    class Level(TextChoices):
        """等级"""

        LEVEL0 = ('0', '普通客户')
        LEVEL1 = ('1', '一级客户')
        LEVEL2 = ('2', '二级客户')
        LEVEL3 = ('3', '三级客户')

    number = CharField(max_length=32, verbose_name='编号')
    name = CharField(max_length=64, verbose_name='名称')
    level = CharField(max_length=32, choices=Level.choices, default=Level.LEVEL0, verbose_name='等级')
    category = ForeignKey('data.ClientCategory', on_delete=SET_NULL, null=True,
                          related_name='clients', verbose_name='客户分类')
    contact = CharField(max_length=64, null=True, blank=True, verbose_name='联系人')
    phone = CharField(max_length=32, blank=True, null=True, verbose_name='手机号')
    email = CharField(max_length=256, blank=True, null=True, verbose_name='邮箱')
    address = CharField(max_length=256, null=True, blank=True, verbose_name='地址')
    remark = CharField(max_length=256, null=True, blank=True, verbose_name='备注')
    order = IntegerField(default=100, verbose_name='顺序')
    is_active = BooleanField(default=True, verbose_name='激活状态')
    initial_arrears_amount = AmountField(default=0, verbose_name='初期欠款金额')
    arrears_amount = AmountField(default=0, verbose_name='欠款金额')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='clients')

    class Meta:
        unique_together = [('number', 'team'), ('name', 'team')]


class Supplier(Model):
    """供应商"""

    number = CharField(max_length=32, verbose_name='编号')
    name = CharField(max_length=64, verbose_name='名称')
    category = ForeignKey('data.SupplierCategory', on_delete=SET_NULL, null=True,
                          related_name='suppliers', verbose_name='供应商分类')
    contact = CharField(max_length=64, null=True, blank=True, verbose_name='联系人')
    phone = CharField(max_length=32, blank=True, null=True, verbose_name='手机号')
    email = CharField(max_length=256, blank=True, null=True, verbose_name='邮箱')
    address = CharField(max_length=256, null=True, blank=True, verbose_name='地址')
    bank_account = CharField(max_length=64, null=True, blank=True, verbose_name='银行账户')
    bank_name = CharField(max_length=64, null=True, blank=True, verbose_name='开户行')
    remark = CharField(max_length=256, null=True, blank=True, verbose_name='备注')
    order = IntegerField(default=100, verbose_name='顺序')
    is_active = BooleanField(default=True, verbose_name='激活状态')
    initial_arrears_amount = AmountField(default=0, verbose_name='初期欠款金额')
    arrears_amount = AmountField(default=0, verbose_name='欠款金额')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='suppliers')

    class Meta:
        unique_together = [('number', 'team'), ('name', 'team')]


class Account(Model):
    """结算账户"""

    class Type(TextChoices):
        """账户类型"""

        CASH = ('cash', '现金')
        ALIPAY = ('alipay', '支付宝')
        WECHAT = ('wechat', '微信')
        BANK_ACCOUNT = ('bank_account', '银行账户')
        OTHER = ('other', '其他')

    number = CharField(max_length=32, verbose_name='编号')
    name = CharField(max_length=64, verbose_name='名称')
    type = CharField(max_length=32, choices=Type.choices, verbose_name='账户类型')
    holder = CharField(max_length=64, null=True, blank=True, verbose_name='开户人')
    remark = CharField(max_length=256, null=True, blank=True, verbose_name='备注')
    order = IntegerField(default=100, verbose_name='顺序')
    is_active = BooleanField(default=True, verbose_name='激活状态')
    initial_balance_amount = AmountField(default=0, verbose_name='初期余额')
    balance_amount = AmountField(default=0, verbose_name='余额')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='accounts')

    class Meta:
        unique_together = [('number', 'team'), ('name', 'team')]


class ChargeItem(Model):
    """收支项目"""

    class Type(TextChoices):
        """收支类型"""

        INCOME = ('income', '收入')
        EXPENDITURE = ('expenditure', '支出')

    name = CharField(max_length=64, verbose_name='名称')
    type = CharField(max_length=32, choices=Type.choices, verbose_name='收支类型')
    remark = CharField(max_length=256, null=True, blank=True, verbose_name='备注')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='charge_items')

    class Meta:
        unique_together = [('name', 'team')]


class ClientCategory(Model):
    """客户分类"""

    name = CharField(max_length=64, verbose_name='名称')
    remark = CharField(max_length=256, null=True, blank=True, verbose_name='备注')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='client_categories')

    class Meta:
        unique_together = [('name', 'team')]


class SupplierCategory(Model):
    """供应商分类"""

    name = CharField(max_length=64, verbose_name='名称')
    remark = CharField(max_length=256, null=True, blank=True, verbose_name='备注')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='supplier_categories')

    class Meta:
        unique_together = [('name', 'team')]


class GoodsCategory(Model):
    """商品分类"""

    name = CharField(max_length=64, verbose_name='名称')
    remark = CharField(max_length=256, null=True, blank=True, verbose_name='备注')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='goods_categories')

    class Meta:
        unique_together = [('name', 'team')]


class GoodsUnit(Model):
    """商品单位"""

    name = CharField(max_length=64, verbose_name='名称')
    remark = CharField(max_length=256, null=True, blank=True, verbose_name='备注')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='goods_units')

    class Meta:
        unique_together = [('name', 'team')]


__all__ = [
    'Warehouse', 'Client', 'Supplier', 'Account',
    'ChargeItem', 'ClientCategory', 'SupplierCategory', 'GoodsCategory', 'GoodsUnit',
]
