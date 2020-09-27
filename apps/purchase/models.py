from django.db import models


class Supplier(models.Model):
    """供应商"""
    name = models.CharField(max_length=48)
    manager = models.CharField(max_length=24, null=True, blank=True)
    phone = models.CharField(max_length=12, null=True, blank=True)
    address = models.CharField(max_length=48, null=True, blank=True)
    mailbox = models.CharField(max_length=48, null=True, blank=True)
    bank_account = models.CharField(max_length=24, null=True, blank=True)  # 银行账户
    bank_name = models.CharField(max_length=24, null=True, blank=True)  # 开户行
    url = models.CharField(max_length=128, null=True, blank=True)
    update_date = models.DateTimeField(auto_now=True)
    default_discount = models.IntegerField(default=100)
    order = models.IntegerField(default=100)
    status = models.BooleanField(default=True)
    remark = models.CharField(max_length=64, null=True, blank=True)
    is_delete = models.BooleanField(default=False)
    teams = models.ForeignKey('user.Teams', models.CASCADE, related_name='supplier_set')


class PurchaseOrder(models.Model):
    """采购单/采购退货单"""
    id = models.CharField(primary_key=True, max_length=20)
    supplier = models.ForeignKey('purchase.Supplier', models.CASCADE, related_name='purchase_order_set')  # 供应商
    supplier_name = models.CharField(max_length=48)
    warehouse = models.ForeignKey('warehouse.Warehouse', models.CASCADE, related_name='purchase_order_set')
    warehouse_name = models.CharField(max_length=48)
    warehouse_address = models.CharField(max_length=128, null=True, blank=True)
    account = models.ForeignKey('account.Account', models.CASCADE, related_name='purchase_order_set')  # 结算账户
    account_name = models.CharField(max_length=48)
    contacts = models.ForeignKey('user.User', models.CASCADE, related_name='purchase_order_set')  # 联系人
    contacts_name = models.CharField(max_length=48)
    contacts_phone = models.CharField(max_length=12)
    amount = models.FloatField(default=0)  # 实付金额
    total_amount = models.FloatField(default=0)  # 应收金额
    total_quantity = models.FloatField(default=0)  # 总数量
    date = models.DateTimeField()
    remark = models.CharField(max_length=64, null=True, blank=True)
    is_done = models.BooleanField(default=False)
    is_return = models.BooleanField(default=False)  # 退货单
    purchase_order = models.ForeignKey('purchase.PurchaseOrder', models.CASCADE, related_name='return_order_set', null=True)
    teams = models.ForeignKey('user.Teams', models.CASCADE, related_name='purchase_order_set')


class PurchaseGoods(models.Model):
    """采购商品"""
    code = models.CharField(max_length=36)
    name = models.CharField(max_length=24)
    specification = models.CharField(max_length=32, null=True, blank=True)  # 规格型号
    unit = models.CharField(max_length=16, null=True, blank=True)  # 单位
    purchase_price = models.FloatField(default=0)
    quantity = models.FloatField(default=0)
    discount = models.FloatField(default=0)  # 折扣
    discount_price = models.FloatField(default=0)  # 折扣价
    amount = models.FloatField(default=0)  # 金额
    discount_amount = models.FloatField(default=0)  # 折扣金额
    goods = models.ForeignKey('goods.Goods', models.CASCADE, related_name='purchase_goods_set')
    purchase_order = models.ForeignKey('purchase.PurchaseOrder', models.CASCADE, related_name='goods_set')


class PaymentRecord(models.Model):
    """付款记录"""
    date = models.DateTimeField(auto_now_add=True)
    amount = models.FloatField(default=0)
    purchase_order = models.ForeignKey('purchase.PurchaseOrder', models.CASCADE, related_name='payment_records')
    account = models.ForeignKey('account.Account', models.CASCADE, related_name='purchase_payment_records')  # 结算账户
    account_name = models.CharField(max_length=48)
    remark = models.CharField(max_length=64, null=True, blank=True)


class ChangeRecord(models.Model):
    """进价变更记录"""
    create_datetime = models.DateTimeField(auto_now_add=True)
    goods = models.ForeignKey('goods.Goods', models.CASCADE, related_name='change_records')
    goods_code = models.CharField(max_length=36)
    goods_name = models.CharField(max_length=128)
    specification = models.CharField(max_length=32, null=True, blank=True)  # 规格型号
    unit = models.CharField(max_length=16, null=True, blank=True)  # 单位
    change_method = models.CharField(max_length=8)
    before_change = models.FloatField()
    after_change = models.FloatField()
    operator = models.ForeignKey('user.User', models.CASCADE, related_name='change_records')
    relation_order = models.ForeignKey('purchase.PurchaseOrder', models.CASCADE, related_name='change_records', null=True)
    teams = models.ForeignKey('user.Teams', models.CASCADE, related_name='change_records')
