from django.db import models


class Warehouse(models.Model):
    """仓库/门店"""
    name = models.CharField(max_length=48, verbose_name='名称')
    manager = models.ForeignKey('user.User', models.CASCADE, related_name='warehouse_set', null=True, verbose_name='管理员')
    remark = models.CharField(max_length=64, null=True, blank=True, verbose_name='备注')
    address = models.CharField(max_length=128, null=True, blank=True, verbose_name='地址')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_date = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    order = models.IntegerField(default=100, verbose_name='排序')
    status = models.BooleanField(default=True, verbose_name='状态')
    is_delete = models.BooleanField(default=False, verbose_name='删除状态')
    teams = models.ForeignKey('user.Teams', models.CASCADE, related_name='warehouse_set')


class Inventory(models.Model):
    """库存"""
    goods = models.ForeignKey('goods.Goods', models.CASCADE, related_name='inventory_set', verbose_name='商品')
    warehouse = models.ForeignKey('warehouse.Warehouse', models.CASCADE, related_name='inventory_set', verbose_name='仓库')
    quantity = models.FloatField(default=0, verbose_name='数量')
    teams = models.ForeignKey('user.Teams', models.CASCADE, related_name='inventory_set')


class Flow(models.Model):
    """库存流水"""
    create_datetime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    goods = models.ForeignKey('goods.Goods', models.CASCADE, related_name='flows', verbose_name='商品')
    goods_code = models.CharField(max_length=36, verbose_name='商品编号')
    goods_name = models.CharField(max_length=128, verbose_name='商品名称')
    specification = models.CharField(max_length=32, null=True, blank=True, verbose_name='规格')
    unit = models.CharField(max_length=16, null=True, blank=True, verbose_name='单位')
    warehouse = models.ForeignKey('warehouse.Warehouse', models.CASCADE, related_name='flows', verbose_name='仓库')
    warehouse_name = models.CharField(max_length=48, verbose_name='仓库名称')
    change_quantity = models.FloatField(default=0, verbose_name='改变数量')
    remain_quantity = models.FloatField(default=0, verbose_name='剩余数量')
    type = models.CharField(max_length=12, verbose_name='类型')
    operator = models.ForeignKey('user.User', models.CASCADE, related_name='flows', verbose_name='操作人')
    teams = models.ForeignKey('user.Teams', models.CASCADE, related_name='flows')

    # 关联单
    requisition = models.ForeignKey('warehouse.Requisition', models.CASCADE, related_name='flows', null=True, verbose_name='调拨单')
    counting_list = models.ForeignKey('warehouse.CountingList', models.CASCADE, related_name='flows', null=True, verbose_name='盘点单')
    purchase_order = models.ForeignKey('purchase.PurchaseOrder', models.CASCADE, related_name='flows', null=True, verbose_name='采购单')
    sales_order = models.ForeignKey('sales.SalesOrder', models.CASCADE, related_name='flows', null=True, verbose_name='销售单')


class CountingList(models.Model):
    """盘点单"""
    id = models.CharField(primary_key=True, max_length=20, verbose_name='编号')
    warehouse = models.ForeignKey('warehouse.Warehouse', models.CASCADE, related_name='counting_list_set', verbose_name='仓库')
    warehouse_name = models.CharField(max_length=48, verbose_name='仓库名称')
    total_quantity = models.FloatField(default=0, verbose_name='盘点总数')
    profit_quantity = models.FloatField(default=0, verbose_name='盈亏数量')  
    profit_amount = models.FloatField(default=0, verbose_name='盈亏金额')
    date = models.DateTimeField(auto_now_add=True, verbose_name='日期')
    remark = models.CharField(max_length=64, null=True, blank=True, verbose_name='备注')
    teams = models.ForeignKey('user.Teams', models.CASCADE, related_name='counting_list_set')


class CountingListGoods(models.Model):
    """盘点单商品"""
    code = models.CharField(max_length=36, verbose_name='商品编号')
    name = models.CharField(max_length=128, verbose_name='商品名称')
    specification = models.CharField(max_length=32, null=True, blank=True, verbose_name='规格')
    unit = models.CharField(max_length=16, null=True, blank=True, verbose_name='单位')
    quantity = models.FloatField(default=0, verbose_name='数量')
    before_counting = models.FloatField(default=0, verbose_name='盘点前数量')
    purchase_price = models.FloatField(default=0, verbose_name='采购价')
    goods = models.ForeignKey('goods.Goods', models.CASCADE, related_name='counting_list_goods_set', verbose_name='商品')
    counting_list = models.ForeignKey('warehouse.CountingList', models.CASCADE, related_name='goods_set', verbose_name='盘点单')


class Requisition(models.Model):
    """调拨单"""
    id = models.CharField(primary_key=True, max_length=20, verbose_name='编号')
    out_warehouse = models.ForeignKey('warehouse.Warehouse', models.CASCADE, related_name='into_requisitions', verbose_name='调出仓库')
    out_warehouse_name = models.CharField(max_length=48, verbose_name='调出仓库名称')
    into_warehouse = models.ForeignKey('warehouse.Warehouse', models.CASCADE, related_name='out_requisitions', verbose_name='调入仓库')
    into_warehouse_name = models.CharField(max_length=48, verbose_name='调入仓库名称')
    total_quantity = models.FloatField(default=0, verbose_name='总数量')
    date = models.DateTimeField(verbose_name='日期')
    remark = models.CharField(max_length=64, null=True, blank=True, verbose_name='备注')
    teams = models.ForeignKey('user.Teams', models.CASCADE, related_name='requisition_set')


class RequisitionGoods(models.Model):
    """调拨单商品"""
    code = models.CharField(max_length=36, verbose_name='商品编号')
    name = models.CharField(max_length=128, verbose_name='商品名称')
    specification = models.CharField(max_length=32, null=True, blank=True, verbose_name='规格')
    unit = models.CharField(max_length=16, null=True, blank=True, verbose_name='单位')
    quantity = models.FloatField(default=0, verbose_name='数量')
    goods = models.ForeignKey('goods.Goods', models.CASCADE, related_name='requisition_goods_set', verbose_name='商品')
    requisition = models.ForeignKey('warehouse.Requisition', models.CASCADE, related_name='goods_set', verbose_name='调拨单')
