from extensions.serializers import *


class CSRFTokenResponse(Serializer):
    token = CharField(label='令牌')


class LoginRequest(Serializer):
    username = CharField(label='用户名')
    password = CharField(label='密码')


class SuperUserInfoResponse(Serializer):
    id = IntegerField(label='用户ID')
    username = CharField(label='用户名')


__all__ = [
    'CSRFTokenResponse', 'LoginRequest', 'SuperUserInfoResponse',
]
