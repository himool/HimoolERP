from django_mysql.models import JSONField
from django.db import models


class Role(models.Model):
    """角色"""
    name = models.CharField(max_length=48)
    remark = models.CharField(max_length=48, null=True, blank=True)
    permissions = JSONField()
    teams = models.ForeignKey('user.Teams', models.CASCADE, related_name='roles')


class Account(models.Model):
    """结算账户"""
    name = models.CharField(max_length=48)  # 账户名称
    account = models.CharField(max_length=48, null=True, blank=True)  # 账号
    holder = models.CharField(max_length=48, null=True, blank=True)  # 开户人
    warehouse = models.ForeignKey('warehouse.Warehouse', models.CASCADE, null=True)
    type = models.CharField(max_length=12)
    order = models.IntegerField(default=100)
    status = models.BooleanField(default=True)
    remark = models.CharField(max_length=64, null=True, blank=True)
    is_delete = models.BooleanField(default=False)
    teams = models.ForeignKey('user.Teams', models.CASCADE, related_name='accounts')


class Bookkeeping(models.Model):
    """记账"""
    create_datetime = models.DateTimeField(auto_now_add=True)
    account = models.ForeignKey('account.Account', models.CASCADE, related_name='bookkeeping_set')
    amount = models.FloatField(default=0)  # 收入支出
    recorder = models.ForeignKey('user.User', models.CASCADE, related_name='bookkeeping_set')
    remark = models.CharField(max_length=64, null=True, blank=True)
    teams = models.ForeignKey('user.Teams', models.CASCADE, related_name='bookkeeping_set')
