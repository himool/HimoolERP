from extensions.serializers import *


class LoginRequest(Serializer):
    username = CharField(label='用户名')
    password = CharField(label='密码')


class SuperUserInfoResponse(Serializer):
    id = IntegerField(label='用户ID')
    username = CharField(label='用户名')
    name = CharField(label='名称')


__all__ = [
    'LoginRequest', 'SuperUserInfoResponse',
]
