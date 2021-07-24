from django.db import models


class SalesOrder(models.Model):
    """销售单"""
    id = models.CharField(primary_key=True, max_length=20, verbose_name='编号')
    date = models.DateField(verbose_name='日期')
    seller = models.ForeignKey('user.User', models.CASCADE, related_name='sales_order_set', verbose_name='销售员')
    seller_username = models.CharField(max_length=48, verbose_name='销售员用户名')
    warehouse = models.ForeignKey('warehouse.Warehouse', models.CASCADE, related_name='sales_order_set', verbose_name='仓库')
    warehouse_name = models.CharField(max_length=48, verbose_name='仓库名称')
    account = models.ForeignKey('account.Account', models.CASCADE, related_name='sales_order_set', verbose_name='结算账户')
    account_name = models.CharField(max_length=48, verbose_name='结算账户名称')
    discount = models.FloatField(default=100, verbose_name='整单折扣')
    amount = models.FloatField(default=0, verbose_name='实收金额')
    total_amount = models.FloatField(default=0, verbose_name='应收金额')
    total_quantity = models.FloatField(default=0, verbose_name='总数量')
    client = models.ForeignKey('sales.Client', models.CASCADE, related_name='sales_order_set', null=True, verbose_name='客户')
    client_phone = models.CharField(max_length=16, null=True, blank=True, verbose_name='客户电话')
    client_contacts = models.CharField(max_length=16, null=True, blank=True, verbose_name='客户联系人')
    client_name = models.CharField(max_length=16, null=True, blank=True, verbose_name='客户名称')
    client_address = models.CharField(max_length=64, null=True, blank=True, verbose_name='客户地址')
    remark = models.CharField(max_length=64, null=True, blank=True, verbose_name='备注')
    is_done = models.BooleanField(default=False, verbose_name='完成状态')
    is_return = models.BooleanField(default=False, verbose_name='退货状态')
    sales_order = models.ForeignKey('sales.SalesOrder', models.CASCADE, related_name='return_order_set', null=True, verbose_name='销售单')
    teams = models.ForeignKey('user.Teams', models.CASCADE, related_name='sales_order_set')


class SalesGoods(models.Model):
    """销售商品"""
    code = models.CharField(max_length=36, verbose_name='商品编号')
    name = models.CharField(max_length=24, verbose_name='商品名称')
    specification = models.CharField(max_length=32, null=True, blank=True, verbose_name='规格')
    unit = models.CharField(max_length=16, null=True, blank=True, verbose_name='单位')
    quantity = models.FloatField(default=0, verbose_name='数量')
    purchase_price = models.FloatField(default=0, verbose_name='采购价')
    retail_price = models.FloatField(default=0, verbose_name='零售价')
    amount = models.FloatField(default=0, verbose_name='金额')
    remark = models.CharField(max_length=64, null=True, blank=True, verbose_name='备注')
    goods = models.ForeignKey('goods.Goods', models.CASCADE, related_name='sales_goods_set', verbose_name='商品')
    sales_order = models.ForeignKey('sales.SalesOrder', models.CASCADE, related_name='goods_set', verbose_name='销售单')


class PaymentRecord(models.Model):
    """付款记录"""
    date = models.DateTimeField(auto_now_add=True, verbose_name='日期')
    amount = models.FloatField(default=0, verbose_name='金额')
    sales_order = models.ForeignKey('sales.SalesOrder', models.CASCADE, related_name='payment_records', verbose_name='销售单')
    account = models.ForeignKey('account.Account', models.CASCADE, related_name='sales_payment_records', verbose_name='结算账户')
    account_name = models.CharField(max_length=48, verbose_name='结算账户名称')
    remark = models.CharField(max_length=64, null=True, blank=True, verbose_name='备注')


class SalesTask(models.Model):
    """销售任务"""
    goods = models.ForeignKey('goods.Goods', models.CASCADE, related_name='sales_tasks', verbose_name='商品')
    warehouse = models.ForeignKey('warehouse.Warehouse', models.CASCADE, related_name='sales_tasks', verbose_name='仓库')
    quantity = models.FloatField(default=0, verbose_name='任务数量')
    start_date = models.DateTimeField(verbose_name='开始日期')
    end_date = models.DateTimeField(verbose_name='结束日期')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    teams = models.ForeignKey('user.Teams', models.CASCADE, related_name='sales_tasks')


class Client(models.Model):
    """客户"""
    phone = models.CharField(max_length=16, verbose_name='手机号')
    name = models.CharField(max_length=24, null=True, blank=True, verbose_name='名称')
    contacts = models.CharField(max_length=24, null=True, blank=True, verbose_name='联系人')
    address = models.CharField(max_length=64, null=True, blank=True, verbose_name='地址')
    email = models.CharField(max_length=48, null=True, blank=True, verbose_name='邮箱')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    is_delete = models.BooleanField(default=False, verbose_name='删除状态')
    teams = models.ForeignKey('user.Teams', models.CASCADE, related_name='clients')
