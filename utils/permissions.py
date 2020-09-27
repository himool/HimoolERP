from rest_framework import permissions


class BasePermission(permissions.BasePermission):
    message = {'message': '无权限'}

    def has_permission(self, request, view):
        if request.method not in self.view_set:
            return True

        roles = request.user.roles.all()
        if not roles:  # 没有设置角色默认拥有全部权限
            return True

        permission = self.permission if hasattr(self, 'permission') else f'{self.name}_{request.method}'
        for role in roles:
            if permission in role.permissions:
                return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        return request.user.teams == obj.teams


class IsAuthenticated(permissions.IsAuthenticated):
    message = {'message': '未登录'}


class PurchasePricePermission(BasePermission):
    name = 'PURCHASE_PRICE'
    view_set = ('GET',)
    permission = 'PURCHASE_PRICE_GET'
