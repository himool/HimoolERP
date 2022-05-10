from rest_framework.viewsets import ViewSet, ModelViewSet
from extensions.common.schema import *
from extensions.common.base import *
from extensions.permissions import *
from extensions.exceptions import *
from apps.manage.serializers import *
from apps.manage.schemas import *
from apps.manage.models import *
from apps.system.models import *
from django.contrib import auth


class SuperUserActionViewSet(ViewSet):
    """管理员操作"""

    @extend_schema(request=LoginRequest, responses={204: None})
    @action(detail=False, methods=['post'])
    def login(self, request, *args, **kwargs):
        """登录"""

        serializer = LoginRequest(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        username = validated_data['username']
        password = validated_data['password']

        if not (super_user := auth.authenticate(username=username, password=password)):
            raise ValidationError('账号密码错误')

        auth.login(request, super_user)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @extend_schema(request=None, responses={204: None})
    @action(detail=False, methods=['post'])
    def logout(self, request, *args, **kwargs):
        """登出"""

        auth.logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class TeamViewSet(ModelViewSet):
    serializer_class = TeamSerializer
    permission_classes = [IsSuperUser]
    search_fields = ['number']
    ordering_fields = ['id', 'number', 'expiry_time', 'create_time']
    queryset = Team.objects.all()

    def get_serializer_class(self):
        if self.method == 'POST':
            return TeamCreateSerializer
        return super().get_serializer_class()


class DeviceViewSet(ModelViewSet):
    serializer_class = DeviceSerializer
    permission_classes = [IsSuperUser]
    search_fields = ['number', 'name', 'serial_number']
    ordering_fields = ['id', 'number', 'name', 'serial_number']
    queryset = Device.objects.all()


__all__ = [
    'SuperUserActionViewSet', 'TeamViewSet', 'DeviceViewSet',
]
