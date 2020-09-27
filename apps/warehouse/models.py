from django.db import models


class Warehouse(models.Model):
    """仓库/门店"""
    name = models.CharField(max_length=48)
    manager = models.ForeignKey('user.User', models.CASCADE, related_name='warehouse_set', null=True)
    remark = models.CharField(max_length=64, null=True, blank=True)
    type = models.CharField(max_length=16)  # 仓库/门店
    address = models.CharField(max_length=128, null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    order = models.IntegerField(default=100)
    status = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)
    teams = models.ForeignKey('user.Teams', models.CASCADE, related_name='warehouse_set')


class Inventory(models.Model):
    """库存"""
    goods = models.ForeignKey('goods.Goods', models.CASCADE, related_name='inventory_set')
    warehouse = models.ForeignKey('warehouse.Warehouse', models.CASCADE, related_name='inventory_set')
    quantity = models.FloatField(default=0)
    teams = models.ForeignKey('user.Teams', models.CASCADE, related_name='inventory_set')


class Flow(models.Model):
    """库存流水"""
    create_datetime = models.DateTimeField(auto_now_add=True)
    goods = models.ForeignKey('goods.Goods', models.CASCADE, related_name='flows')
    goods_code = models.CharField(max_length=36)
    goods_name = models.CharField(max_length=128)
    specification = models.CharField(max_length=32, null=True, blank=True)  # 规格型号
    unit = models.CharField(max_length=16, null=True, blank=True)  # 单位
    warehouse = models.ForeignKey('warehouse.Warehouse', models.CASCADE, related_name='flows')
    warehouse_name = models.CharField(max_length=48)
    change_quantity = models.FloatField(default=0)
    remain_quantity = models.FloatField(default=0)
    type = models.CharField(max_length=12)
    operator = models.ForeignKey('user.User', models.CASCADE, related_name='flows')
    teams = models.ForeignKey('user.Teams', models.CASCADE, related_name='flows')

    # 关联单
    requisition = models.ForeignKey('warehouse.Requisition', models.CASCADE, related_name='flows', null=True)
    counting_list = models.ForeignKey('warehouse.CountingList', models.CASCADE, related_name='flows', null=True)
    purchase_order = models.ForeignKey('purchase.PurchaseOrder', models.CASCADE, related_name='flows', null=True)
    sales_order = models.ForeignKey('sales.SalesOrder', models.CASCADE, related_name='flows', null=True)


class CountingList(models.Model):
    """盘点单"""
    id = models.CharField(primary_key=True, max_length=20)
    warehouse = models.ForeignKey('warehouse.Warehouse', models.CASCADE, related_name='counting_list_set')
    warehouse_name = models.CharField(max_length=48)
    total_quantity = models.FloatField(default=0)  # 盘点总数
    profit_quantity = models.FloatField(default=0)  
    profit_amount = models.FloatField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    remark = models.CharField(max_length=64, null=True, blank=True)
    teams = models.ForeignKey('user.Teams', models.CASCADE, related_name='counting_list_set')


class CountingListGoods(models.Model):
    """盘点单商品"""
    code = models.CharField(max_length=36)
    name = models.CharField(max_length=128)
    specification = models.CharField(max_length=32, null=True, blank=True)  # 规格型号
    unit = models.CharField(max_length=16, null=True, blank=True)  # 单位
    quantity = models.FloatField(default=0)  # 盘点数量
    before_counting = models.FloatField(default=0)  # 盘点前数量
    purchase_price = models.FloatField(default=0)
    goods = models.ForeignKey('goods.Goods', models.CASCADE, related_name='counting_list_goods_set')
    counting_list = models.ForeignKey('warehouse.CountingList', models.CASCADE, related_name='goods_set')


class Requisition(models.Model):
    """调拨单"""
    id = models.CharField(primary_key=True, max_length=20)
    out_warehouse = models.ForeignKey('warehouse.Warehouse', models.CASCADE, related_name='into_requisitions')
    out_warehouse_name = models.CharField(max_length=48)
    into_warehouse = models.ForeignKey('warehouse.Warehouse', models.CASCADE, related_name='out_requisitions')
    into_warehouse_name = models.CharField(max_length=48)
    total_quantity = models.FloatField(default=0)  # 总数量
    date = models.DateTimeField()
    remark = models.CharField(max_length=64, null=True, blank=True)
    teams = models.ForeignKey('user.Teams', models.CASCADE, related_name='requisition_set')


class RequisitionGoods(models.Model):
    """调拨单商品"""
    code = models.CharField(max_length=36)
    name = models.CharField(max_length=128)
    specification = models.CharField(max_length=32, null=True, blank=True)  # 规格型号
    unit = models.CharField(max_length=16, null=True, blank=True)  # 单位
    quantity = models.FloatField(default=0)
    goods = models.ForeignKey('goods.Goods', models.CASCADE, related_name='requisition_goods_set')
    requisition = models.ForeignKey('warehouse.Requisition', models.CASCADE, related_name='goods_set')
