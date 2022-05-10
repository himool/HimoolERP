from extensions.common.base import *
from extensions.exceptions import *
from apps.manage.models import *
from apps.system.models import *
from rest_framework.serializers import ModelSerializer, CharField
from django.contrib.auth.hashers import make_password


class TeamSerializer(ModelSerializer):

    class Meta:
        model = Team
        read_only_fields = ['id']
        fields = ['number', 'expiry_time', 'user_quantity', *read_only_fields]

    def validate_number(self, value):
        self.validate_unique({'number': value}, message=f'公司编号[{value}]已存在')
        return value


class TeamCreateSerializer(ModelSerializer):
    username = CharField(max_length=32, label='用户名')
    password = CharField(max_length=256, label='密码')
    name = CharField(max_length=64, label='名称')

    class Meta:
        model = Team
        read_only_fields = ['id']
        fields = ['number', 'expiry_time', 'user_quantity', 'username', 'password', 'name', *read_only_fields]

    def validate_number(self, value):
        self.validate_unique({'number': value}, message=f'公司编号[{value}]已存在')
        return value

    @transaction.atomic
    def create(self, validated_data):
        username = validated_data.pop('username')
        password = validated_data.pop('password')
        password = make_password(password)
        name = validated_data.pop('name')

        team = super().create(validated_data)
        User.objects.create(username=username, password=password, name=name, is_manager=True, team=team)

        return team


class DeviceSerializer(ModelSerializer):

    class Meta:
        model = Device
        read_only_fields = ['id']
        fields = ['number', 'name', 'model', 'serial_number', 'account_ownership', *read_only_fields]

    def validate_number(self, value):
        self.validate_unique({'number': value}, message=f'编号[{value}]已存在')
        return value


__all__ = [
    'TeamSerializer', 'TeamCreateSerializer', 'DeviceSerializer',
]
