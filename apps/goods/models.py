from django.db import models


class Goods(models.Model):
    """商品"""
    code = models.CharField(max_length=36)
    name = models.CharField(max_length=128)
    purchase_price = models.FloatField(default=0)
    suggested_retail_price = models.FloatField(default=0)
    retail_price = models.FloatField(default=0)
    inventory_warning_lower_limit = models.FloatField(default=0)
    inventory_warning_upper_limit = models.FloatField(default=5000)
    brand = models.CharField(max_length=48, null=True, blank=True)
    specification = models.CharField(max_length=32, null=True, blank=True)  # 规格型号
    unit = models.CharField(max_length=16, null=True, blank=True)  # 单位
    category = models.ForeignKey('goods.Category', models.CASCADE, related_name='goods', null=True)
    initial_quantity = models.FloatField(default=0)
    order = models.IntegerField(default=100)
    status = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)
    teams = models.ForeignKey('user.Teams', models.CASCADE, related_name='goods_set')


class Category(models.Model):
    """商品分类"""
    name = models.CharField(max_length=24)
    description = models.CharField(max_length=128, null=True, blank=True)
    order = models.IntegerField(default=100)
    teams = models.ForeignKey('user.Teams', models.CASCADE, related_name='category_set')
