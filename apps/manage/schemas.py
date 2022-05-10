from extensions.serializers import *


class LoginRequest(Serializer):
    username = CharField(label='用户名')
    password = CharField(label='密码')


__all__ = [
    'LoginRequest',
]
