from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django_mysql.models import JSONField
from django.db import models


class Teams(models.Model):
    phone = models.CharField(max_length=12, unique=True, verbose_name='手机号')


class UserManager(BaseUserManager):
    def create(self, username, password, **kwargs):
        user = self.model(username=username, **kwargs)
        user.set_password(password)
        user.save(self._db)
        return user


class User(AbstractBaseUser):
    username = models.CharField(max_length=24, unique=True, verbose_name='用户名')
    phone = models.CharField(max_length=12, verbose_name='手机号')
    teams = models.ForeignKey('user.Teams', models.CASCADE, related_name='users', verbose_name='组')

    roles = models.ManyToManyField('account.Role', blank=True, related_name='users', verbose_name='角色')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    is_manager = models.BooleanField(default=True, verbose_name='管理员状态')
    is_delete = models.BooleanField(default=False, verbose_name='删除状态')

    USERNAME_FIELD = 'username'
    objects = UserManager()
