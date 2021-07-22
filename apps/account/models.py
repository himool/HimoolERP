from django_mysql.models import JSONField
from django.db import models


class Role(models.Model):
    """角色"""
    name = models.CharField(max_length=48, verbose_name='名称')
    remark = models.CharField(max_length=48, null=True, blank=True, verbose_name='备注')
    permissions = JSONField(verbose_name='权限')
    teams = models.ForeignKey('user.Teams', models.CASCADE, related_name='roles')


class Account(models.Model):
    """结算账户"""
    name = models.CharField(max_length=48, verbose_name='名称')
    account = models.CharField(max_length=48, null=True, blank=True, verbose_name='账号')
    holder = models.CharField(max_length=48, null=True, blank=True, verbose_name='开户人')
    warehouse = models.ForeignKey('warehouse.Warehouse', models.CASCADE, null=True, verbose_name='仓库')
    type = models.CharField(max_length=12, verbose_name='类型')
    order = models.IntegerField(default=100, verbose_name='排序')
    status = models.BooleanField(default=True, verbose_name='状态')
    remark = models.CharField(max_length=64, null=True, blank=True, verbose_name='备注')
    is_delete = models.BooleanField(default=False, verbose_name='删除状态')
    teams = models.ForeignKey('user.Teams', models.CASCADE, related_name='accounts')


class Bookkeeping(models.Model):
    """记账"""
    create_datetime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    account = models.ForeignKey('account.Account', models.CASCADE, related_name='bookkeeping_set', verbose_name='结算账户')
    amount = models.FloatField(default=0, verbose_name='金额')
    recorder = models.ForeignKey('user.User', models.CASCADE, related_name='bookkeeping_set', verbose_name='记录人')
    remark = models.CharField(max_length=64, null=True, blank=True, verbose_name='备注')
    teams = models.ForeignKey('user.Teams', models.CASCADE, related_name='bookkeeping_set')
