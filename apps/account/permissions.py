from utils.permissions import BasePermission


class RolePermission(BasePermission):
    name = 'ROLE'
    view_set = ('POST', 'PUT', 'DELETE')


class SubuserPermission(BasePermission):
    name = 'SUBUSER'
    view_set = ('POST', 'PUT', 'DELETE')
    permission = 'SUBUSER_POST_PUT_DELETE'
