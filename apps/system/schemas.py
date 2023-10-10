from extensions.serializers import *


class GetTokenRequest(Serializer):
    number = CharField(label='Team 编号')
    username = CharField(label='用户名')
    password = CharField(label='密码')


class GetTokenResponse(Serializer):
    refresh = CharField(label='刷新令牌')
    access = CharField(label='访问令牌')


class RefreshTokenRequest(Serializer):
    refresh = CharField(label='刷新令牌')


class RefreshTokenResponse(Serializer):
    access = CharField(label='访问令牌')


class UserInfoResponse(Serializer):
    id = IntegerField(label='用户ID')
    username = CharField(label='用户名')
    name = CharField(label='名称')
    is_manager = BooleanField(label='管理员状态')
    permissions = JSONField(label='权限')


class SetPasswordRequest(Serializer):
    old_password = CharField(label='旧密码')
    new_password = CharField(label='新密码')


class MakeCodeRequest(Serializer):
    phone = CharField(label='手机号')


class RegisterRequest(Serializer):
    register_city = CharField(label='所在城市')
    register_city_code = ListField(child=CharField(), label='所在城市代码')
    phone = CharField(label='手机号')
    code = CharField(label='验证码')
    number = CharField(label='公司编号')
    username = CharField(label='用户名')
    password = CharField(label='密码')


class AdminUpdateAccountRequest(Serializer):
    company = CharField(label='公司编号')
    username = CharField(label='用户名')
    expiry_date = DateField(label='到期日期')


__all__ = [
    'GetTokenRequest', 'GetTokenResponse',
    'RefreshTokenRequest', 'RefreshTokenResponse',
    'UserInfoResponse', 'SetPasswordRequest',
    'MakeCodeRequest', 'RegisterRequest', 'AdminUpdateAccountRequest',
]
