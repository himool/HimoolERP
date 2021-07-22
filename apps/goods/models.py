from django.db import models


class Goods(models.Model):
    """商品"""
    code = models.CharField(max_length=36, verbose_name='编号')
    name = models.CharField(max_length=128, verbose_name='名称')
    purchase_price = models.FloatField(default=0, verbose_name='采购价')
    suggested_retail_price = models.FloatField(default=0, verbose_name='建议零售价')
    retail_price = models.FloatField(default=0, verbose_name='零售价')
    inventory_warning_lower_limit = models.FloatField(default=0, verbose_name='库存下限')
    inventory_warning_upper_limit = models.FloatField(default=5000, verbose_name='库存上限')
    brand = models.CharField(max_length=48, null=True, blank=True, verbose_name='品牌')
    specification = models.CharField(max_length=32, null=True, blank=True, verbose_name='规格')
    unit = models.CharField(max_length=16, null=True, blank=True, verbose_name='单位')
    category = models.ForeignKey('goods.Category', models.CASCADE, related_name='goods', null=True, verbose_name='分类')
    initial_quantity = models.FloatField(default=0, verbose_name='初始库存')
    order = models.IntegerField(default=100, verbose_name='排序')
    status = models.BooleanField(default=True, verbose_name='状态')
    is_delete = models.BooleanField(default=False, verbose_name='删除状态')
    teams = models.ForeignKey('user.Teams', models.CASCADE, related_name='goods_set')


class Category(models.Model):
    """商品分类"""
    name = models.CharField(max_length=24, verbose_name='名称')
    description = models.CharField(max_length=128, null=True, blank=True, verbose_name='描述')
    order = models.IntegerField(default=100, verbose_name='排序')
    teams = models.ForeignKey('user.Teams', models.CASCADE, related_name='category_set')
