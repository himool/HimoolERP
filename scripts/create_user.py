from django.contrib.auth.hashers import make_password
from django.db import transaction
from apps.system.models import *
import pendulum


@transaction.atomic
def create_user(team_number, register_phone, register_city, expiry_time, username, password, is_active=True):
    team = Team.objects.create(
        number=team_number,
        expiry_time=expiry_time,
        register_phone=register_phone,
        register_city=register_city,
        is_active=is_active)

    User.objects.create(team=team, username=username, password=make_password(password), name=username, is_manager=True)


def run(*args):
    number = input('编号: ')
    username = input('用户名: ')
    password = input('密码: ')
    activation_days = input('激活天数: ')
    expiry_time = pendulum.now().add(days=float(activation_days))

    create_user(number, None, None, expiry_time, username, password)
