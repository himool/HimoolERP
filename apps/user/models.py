from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django_mysql.models import JSONField
from django.db import models


class Teams(models.Model):
    phone = models.CharField(max_length=12, unique=True)
    company_name = models.CharField(max_length=48)
    # end_datetime = models.DateTimeField()


class UserManager(BaseUserManager):
    def create(self, username, password, **kwargs):
        user = self.model(username=username, **kwargs)
        user.set_password(password)
        user.save(self._db)
        return user


class User(AbstractBaseUser):
    username = models.CharField(primary_key=True, max_length=24)
    name = models.CharField(max_length=48)
    phone = models.CharField(max_length=12)
    teams = models.ForeignKey('user.Teams', models.CASCADE, related_name='users')

    roles = models.ManyToManyField('account.Role', related_name='users')
    create_date = models.DateTimeField(auto_now_add=True)
    is_boss = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    objects = UserManager()
