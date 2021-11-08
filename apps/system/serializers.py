from django.contrib.auth.hashers import make_password
from extensions.serializers import *
from extensions.exceptions import *
from apps.system.models import *


class PermissionSerializer(BaseSerializer):

    class Meta:
        model = Permission
        fields = ['id', 'name', 'code']


class PermissionTypeSerializer(BaseSerializer):
    permission_items = PermissionSerializer(source='permissions', many=True, label='权限')

    class Meta:
        model = PermissionType
        fields = ['id', 'name', 'permission_items']


class RoleSerializer(BaseSerializer):

    class Meta:
        model = Role
        read_only_fields = ['id']
        fields = ['name', 'remark', 'permissions', *read_only_fields]


class UserSerializer(BaseSerializer):

    class Meta:
        model = User
        read_only_fields = ['id', 'is_manager', 'create_time']
        fields = ['username', 'name', 'phone', 'email', 'sex', 'roles', 'is_active', *read_only_fields]

    def validate_username(self, value):
        self.validate_unique({'username': value}, message=f'用户名[{value}]已存在')
        return value

    def validate_roles(self, instances):
        instances = self.validate_foreign_key_set(Role, instances)
        return instances

    def create(self, validated_data):
        validated_data['password'] = make_password(self.team.number)
        return super().create(validated_data)


__all__ = [
    'PermissionSerializer', 'PermissionTypeSerializer', 'RoleSerializer', 'UserSerializer',
]
