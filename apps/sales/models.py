from django.db import models


class SalesOrder(models.Model):
    """销售单"""
    id = models.CharField(primary_key=True, max_length=20)
    date = models.DateTimeField()
    seller = models.ForeignKey('user.User', models.CASCADE, related_name='sales_order_set')  # 销售员
    seller_username = models.CharField(max_length=48)
    warehouse = models.ForeignKey('warehouse.Warehouse', models.CASCADE, related_name='sales_order_set')
    warehouse_name = models.CharField(max_length=48)
    account = models.ForeignKey('account.Account', models.CASCADE, related_name='sales_order_set')  # 结算账户
    account_name = models.CharField(max_length=48)
    discount = models.FloatField(default=100)  # 整单折扣
    amount = models.FloatField(default=0)  # 实收金额
    total_amount = models.FloatField(default=0)  # 应收金额
    total_quantity = models.FloatField(default=0)  # 总数量
    client = models.ForeignKey('sales.Client', models.CASCADE, related_name='sales_order_set', null=True)
    client_phone = models.CharField(max_length=16, null=True, blank=True)  # 客户电话
    client_contacts = models.CharField(max_length=16, null=True, blank=True)  # 客户联系人
    client_name = models.CharField(max_length=16, null=True, blank=True)
    client_address = models.CharField(max_length=64, null=True, blank=True)
    remark = models.CharField(max_length=64, null=True, blank=True)
    is_done = models.BooleanField(default=False)
    is_return = models.BooleanField(default=False)  # 退货单
    sales_order = models.ForeignKey('sales.SalesOrder', models.CASCADE, related_name='return_order_set', null=True)
    teams = models.ForeignKey('user.Teams', models.CASCADE, related_name='sales_order_set')


class SalesGoods(models.Model):
    """销售商品"""
    code = models.CharField(max_length=36)
    name = models.CharField(max_length=24)
    specification = models.CharField(max_length=32, null=True, blank=True)  # 规格型号
    unit = models.CharField(max_length=16, null=True, blank=True)  # 单位
    quantity = models.FloatField(default=0)
    purchase_price = models.FloatField(default=0)
    retail_price = models.FloatField(default=0)  # 单价
    amount = models.FloatField(default=0)  # 金额
    remark = models.CharField(max_length=64, null=True, blank=True)
    goods = models.ForeignKey('goods.Goods', models.CASCADE, related_name='sales_goods_set')
    sales_order = models.ForeignKey('sales.SalesOrder', models.CASCADE, related_name='goods_set')


class PaymentRecord(models.Model):
    """付款记录"""
    date = models.DateTimeField(auto_now_add=True)
    amount = models.FloatField(default=0)
    sales_order = models.ForeignKey('sales.SalesOrder', models.CASCADE, related_name='payment_records')
    account = models.ForeignKey('account.Account', models.CASCADE, related_name='sales_payment_records')  # 结算账户
    account_name = models.CharField(max_length=48)
    remark = models.CharField(max_length=64, null=True, blank=True)


class SalesTask(models.Model):
    """销售任务"""
    goods = models.ForeignKey('goods.Goods', models.CASCADE, related_name='sales_tasks')
    warehouse = models.ForeignKey('warehouse.Warehouse', models.CASCADE, related_name='sales_tasks')
    quantity = models.FloatField(default=0)  # 任务数量
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    create_date = models.DateTimeField(auto_now_add=True)
    teams = models.ForeignKey('user.Teams', models.CASCADE, related_name='sales_tasks')


class Client(models.Model):
    """客户"""
    phone = models.CharField(max_length=16)
    name = models.CharField(max_length=24, null=True, blank=True)  # 客户名称
    contacts = models.CharField(max_length=24, null=True, blank=True)  # 联系人
    address = models.CharField(max_length=64, null=True, blank=True)
    mailbox = models.CharField(max_length=48, null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    is_delete = models.BooleanField(default=False)
    teams = models.ForeignKey('user.Teams', models.CASCADE, related_name='clients')
