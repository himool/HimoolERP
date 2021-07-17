from rest_framework.decorators import api_view, action
from rest_framework import status, exceptions
from rest_framework.response import Response
from .models import Teams, User
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
    phone = request.data.get('phone')
    username = request.data.get('username')
    password = request.data.get('password')

    # 数据验证
    if not username or not password or not phone:
        raise exceptions.ValidationError

    if Teams.objects.filter(phone=phone).first():
        raise exceptions.ValidationError({'message': '手机号已被注册'})

    if User.objects.filter(username=username).first():
        raise exceptions.ValidationError({'message': '账号已被注册'})

    teams = Teams.objects.create(phone=phone)
    User.objects.create(phone=phone, username=username, password=password, teams=teams)
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
