from utils.permissions import BasePermission


class SalesOrderPermission(BasePermission):
    name = 'SALES'
    view_set = ('GET', 'POST', 'PUT', 'DELETE')
