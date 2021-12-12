from extensions.exceptions import NotAuthenticated, ValidationError
from rest_framework.permissions import BasePermission
from apps.system.models import User
import pendulum


class IsAuthenticated(BasePermission):

    def has_permission(self, request, view):
        if not isinstance(request.user, User):
            raise NotAuthenticated

        if (expiry_time := request.user.team.expiry_time) < pendulum.now():
            raise ValidationError(f'已到期, 到期日期: {expiry_time}')

        if not (request.user.is_manager or request.user.is_active):
            raise ValidationError('账号未激活, 无法执行任何操作')

        return True


class IsManagerPermission(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_manager


class ModelPermission(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_manager:
            return True

        if self.code in request.user.permissions:
            return True

        return False


class FunctionPermission(BasePermission):
    """功能权限"""

    def has_permission(self, request, view):
        if request.user.is_manager:
            return True

        if self.code in request.user.permissions:
            return True

        return False


class DataPermission:
    """数据权限"""

    @classmethod
    def has_permission(cls, request):
        if request.user.is_manager:
            return True

        if cls.code in request.user.permissions:
            return True
        return False


__all__ = [
    'IsAuthenticated', 'IsManagerPermission',
    'ModelPermission', 'FunctionPermission', 'DataPermission',
]
