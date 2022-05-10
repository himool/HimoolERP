from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from extensions.models import *


class SuperUser(AbstractBaseUser):
    username = CharField(max_length=32, verbose_name='用户名')

    USERNAME_FIELD = 'username'
    objects = BaseUserManager()


class Device(Model):
    """设备"""

    number = CharField(max_length=32, verbose_name='编号')
    name = CharField(max_length=64, verbose_name='名称')
    model = CharField(max_length=64, null=True, blank=True, verbose_name='型号')
    serial_number = CharField(max_length=256, null=True, blank=True, verbose_name='序列号')
    account_ownership = CharField(max_length=256, null=True, blank=True, verbose_name='账号归属')

    class Meta:
        unique_together = [('number', 'team')]


__all__ = [
    'SuperUser', 'Device',
]
