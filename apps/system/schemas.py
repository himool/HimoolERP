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
    username = CharField(label='用户名')
    name = CharField(label='名称')
    is_manager = BooleanField(label='管理员状态')
    permissions = SerializerMethodField(label='权限')

    def get_permissions(self, instance):
        return instance.roles.all().values_list('permissions__code', flat=True)


class SetPasswordRequest(Serializer):
    old_password = CharField(label='旧密码')
    new_password = CharField(label='新密码')


__all__ = [
    'GetTokenRequest', 'GetTokenResponse',
    'RefreshTokenRequest', 'RefreshTokenResponse',
    'UserInfoResponse', 'SetPasswordRequest',
]
