from extensions.exceptions import NotAuthenticated, ValidationError
from rest_framework.permissions import BasePermission
from apps.system.models import Permission, User
import pendulum


class IsAuthenticated(BasePermission):

    def has_permission(self, request, view):
        if not isinstance(request.user, User):
            raise NotAuthenticated

        if (expiry_time := request.user.team.expiry_time) < pendulum.now():
            raise ValidationError(f'已到期, 到期日期: {expiry_time}')

        return True


class IsManagerPermission(IsAuthenticated):

    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.is_manager


class InterfacePermission(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_manager:
            return True

        roles = request.user.roles.all()
        if Permission.objects.filter(roles__in=roles, code=self.code).exists():
            return True
        return False


__all__ = [
    'BasePermission', 'IsAuthenticated', 'IsManagerPermission', 'InterfacePermission',
]
