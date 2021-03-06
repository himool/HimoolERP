from rest_framework.decorators import api_view, action
from oms.settings import captcha_app_key
from rest_framework import status, exceptions
from rest_framework.response import Response
from .models import Teams, User, Captcha
from warehouse.models import Inventory
from rest_framework import viewsets
from django.contrib import auth
from django.db.models import F
import requests
import pendulum
import random
import re


@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = auth.authenticate(username=username, password=password)
    teams = Teams.objects.filter(phone=username).first()
    if not user:
        if not teams:
            raise exceptions.AuthenticationFailed({'message': '账号密码错误'})
        else:
            user = teams.users.filter(is_boss=True).first()
            user = auth.authenticate(username=user.username, password=password)
            if not user:
                raise exceptions.AuthenticationFailed({'message': '账号密码错误'})

    auth.login(request, user)
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def logout(request):
    auth.logout(request)
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def register(request):
    company_name = request.data.get('company_name')
    name = request.data.get('name')
    phone = request.data.get('phone')
    code = request.data.get('code')
    username = request.data.get('username')
    password = request.data.get('password')
    custom_made = request.data.get('custom_made')
    budget = request.data.get('budget')

    # 数据验证
    if not username or not password or not company_name or not name or not phone:
        raise exceptions.ValidationError

    if not code or len(code) != 6 or not re.match(r'^1[3456789]\d{9}$', phone):
        raise exceptions.ValidationError

    # 验证 code
    filters = {
        'phone': phone,
        'code': code,
        'create_datetime__gte': pendulum.now().subtract(minutes=10),
        'create_datetime__lte': pendulum.now(),
    }

    if not Captcha.objects.filter(**filters).first():
        raise exceptions.ValidationError({'message': '验证码错误'})

    if Teams.objects.filter(phone=phone).first():
        raise exceptions.ValidationError({'message': '手机号已被注册'})

    if User.objects.filter(username=username).first():
        raise exceptions.ValidationError({'message': '账号已被注册'})

    teams = Teams.objects.create(phone=phone, company_name=company_name)
    User.objects.create(name=name, phone=phone, username=username,
                        password=password, teams=teams, custom_made=custom_made, budget=budget)
    return Response(status=status.HTTP_201_CREATED)


@api_view(['GET'])
def get_info(request):
    if not request.user.is_authenticated:
        raise exceptions.AuthenticationFailed({'message': '未登录'})

    teams = request.user.teams
    inventory_warning_count = Inventory.objects.filter(
        teams=teams, quantity__lte=F('goods__inventory_warning_lower_limit')).count()
    data = {'username': request.user.username, 'inventory_warning_count': inventory_warning_count}
    return Response(data=data, status=status.HTTP_200_OK)


@api_view(['POST'])
def set_password(request):
    phone = request.data.get('phone')
    code = request.data.get('code')
    password = request.data.get('password')
    confirm = request.data.get('confirm')

    # 数据验证
    if not phone or not password or not confirm or password != confirm:
        raise exceptions.ValidationError

    if not code or len(code) != 6 or not re.match(r'^1[3456789]\d{9}$', phone):
        raise exceptions.ValidationError

    # 验证 code
    filters = {
        'phone': phone,
        'code': code,
        'create_datetime__gte': pendulum.now().subtract(minutes=10),
        'create_datetime__lte': pendulum.now(),
    }

    if not Captcha.objects.filter(**filters).first():
        raise exceptions.ValidationError({'message': '验证码错误'})

    teams = Teams.objects.filter(phone=phone).first()
    if not teams:
        raise exceptions.ValidationError({'message': '账号不存在'})

    user = teams.users.filter(is_boss=True).first()
    user.set_password(password)
    user.save()

    auth.logout(request)
    return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
def get_captcha(request):
    phone = request.GET.get('phone')

    if not phone or not re.match(r'^1[3456789]\d{9}$', phone):
        raise exceptions.ValidationError

    char_range = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'q', 'w', 'e', 'r',
                  't', 'y', 'u', 'i', 'o', 'p', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k',
                  'l', 'z', 'x', 'c', 'v', 'b', 'n', 'm']
    code = ''.join(map(lambda _: random.choice(char_range), range(6)))
    Captcha.objects.create(phone=phone, code=code)

    # 发送短信
    url = 'https://api.jisuapi.com/sms/send'
    resp = requests.get(url, params={
        'appkey': captcha_app_key,
        'mobile': phone,
        'content': f'您的手机验证码是 {code}，本条信息无需回复。【盒木科技】',
    })

    if int(resp.json().get('status', -1)) != 0:
        raise exceptions.APIException({'message': '获取验证码失败'})

    return Response(status=status.HTTP_200_OK)
