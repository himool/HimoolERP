from django.db import models


class Supplier(models.Model):
    """供应商"""
    name = models.CharField(max_length=48, verbose_name='名称')
    manager = models.CharField(max_length=24, null=True, blank=True, verbose_name='管理员')
    phone = models.CharField(max_length=12, null=True, blank=True, verbose_name='手机号')
    address = models.CharField(max_length=48, null=True, blank=True, verbose_name='地址')
    email = models.CharField(max_length=48, null=True, blank=True, verbose_name='邮箱')
    bank_account = models.CharField(max_length=24, null=True, blank=True, verbose_name='银行账户')
    bank_name = models.CharField(max_length=24, null=True, blank=True, verbose_name='开户行')
    url = models.CharField(max_length=128, null=True, blank=True, verbose_name='网址')
    update_date = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    default_discount = models.IntegerField(default=100, verbose_name='默认折扣')
    order = models.IntegerField(default=100, verbose_name='排序')
    status = models.BooleanField(default=True, verbose_name='状态')
    remark = models.CharField(max_length=64, null=True, blank=True, verbose_name='备注')
    is_delete = models.BooleanField(default=False, verbose_name='删除状态')
    teams = models.ForeignKey('user.Teams', models.CASCADE, related_name='supplier_set')


class PurchaseOrder(models.Model):
    """采购单/采购退货单"""
    id = models.CharField(primary_key=True, max_length=20, verbose_name='编号')
    supplier = models.ForeignKey('purchase.Supplier', models.CASCADE, related_name='purchase_order_set', verbose_name='供应商')
    supplier_name = models.CharField(max_length=48, verbose_name='供应商名称')
    warehouse = models.ForeignKey('warehouse.Warehouse', models.CASCADE, related_name='purchase_order_set', verbose_name='仓库')
    warehouse_name = models.CharField(max_length=48, verbose_name='仓库名称')
    warehouse_address = models.CharField(max_length=128, null=True, blank=True, verbose_name='仓库地址')
    account = models.ForeignKey('account.Account', models.CASCADE, related_name='purchase_order_set', verbose_name='结算账户')
    account_name = models.CharField(max_length=48, verbose_name='结算账户名称')
    contacts = models.ForeignKey('user.User', models.CASCADE, related_name='purchase_order_set', verbose_name='联系人')
    contacts_name = models.CharField(max_length=48, verbose_name='联系人名称')
    contacts_phone = models.CharField(max_length=12, verbose_name='联系人电话')
    amount = models.FloatField(default=0, verbose_name='实付金额')
    total_amount = models.FloatField(default=0, verbose_name='应收金额')
    total_quantity = models.FloatField(default=0, verbose_name='总数量')
    date = models.DateField(verbose_name='日期')
    remark = models.CharField(max_length=64, null=True, blank=True, verbose_name='备注')
    is_done = models.BooleanField(default=False, verbose_name='完成状态')
    is_return = models.BooleanField(default=False, verbose_name='退货状态')
    purchase_order = models.ForeignKey('purchase.PurchaseOrder', models.CASCADE, related_name='return_order_set', null=True, verbose_name='采购单')
    teams = models.ForeignKey('user.Teams', models.CASCADE, related_name='purchase_order_set')


class PurchaseGoods(models.Model):
    """采购商品"""
    code = models.CharField(max_length=36, verbose_name='商品编号')
    name = models.CharField(max_length=24, verbose_name='商品名称')
    specification = models.CharField(max_length=32, null=True, blank=True, verbose_name='规格')
    unit = models.CharField(max_length=16, null=True, blank=True, verbose_name='单位')
    purchase_price = models.FloatField(default=0, verbose_name='采购价')
    quantity = models.FloatField(default=0, verbose_name='数量')
    discount = models.FloatField(default=0, verbose_name='折扣')
    discount_price = models.FloatField(default=0, verbose_name='折扣价')
    amount = models.FloatField(default=0, verbose_name='金额')
    discount_amount = models.FloatField(default=0, verbose_name='折扣金额')
    goods = models.ForeignKey('goods.Goods', models.CASCADE, related_name='purchase_goods_set', verbose_name='商品')
    purchase_order = models.ForeignKey('purchase.PurchaseOrder', models.CASCADE, related_name='goods_set')


class PaymentRecord(models.Model):
    """付款记录"""
    date = models.DateTimeField(auto_now_add=True, verbose_name='日期')
    amount = models.FloatField(default=0, verbose_name='金额')
    purchase_order = models.ForeignKey('purchase.PurchaseOrder', models.CASCADE, related_name='payment_records', verbose_name='采购单')
    account = models.ForeignKey('account.Account', models.CASCADE, related_name='purchase_payment_records', verbose_name='结算账户')
    account_name = models.CharField(max_length=48, verbose_name='结算账户名称')
    remark = models.CharField(max_length=64, null=True, blank=True, verbose_name='备注')


class ChangeRecord(models.Model):
    """进价变更记录"""
    create_datetime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    goods = models.ForeignKey('goods.Goods', models.CASCADE, related_name='change_records', verbose_name='商品')
    goods_code = models.CharField(max_length=36, verbose_name='商品编号')
    goods_name = models.CharField(max_length=128, verbose_name='商品名称')
    specification = models.CharField(max_length=32, null=True, blank=True, verbose_name='规格')
    unit = models.CharField(max_length=16, null=True, blank=True, verbose_name='单位')
    change_method = models.CharField(max_length=8, verbose_name='变更方式')
    before_change = models.FloatField(verbose_name='改变前')
    after_change = models.FloatField(verbose_name='改变后')
    operator = models.ForeignKey('user.User', models.CASCADE, related_name='change_records', verbose_name='操作人')
    relation_order = models.ForeignKey('purchase.PurchaseOrder', models.CASCADE, related_name='change_records', null=True, verbose_name='采购单')
    teams = models.ForeignKey('user.Teams', models.CASCADE, related_name='change_records')
