from extensions.permissions import ModelPermission


class SalesOrderPermission(ModelPermission):
    code = 'sales_order'


class SalesReturnOrderPermission(ModelPermission):
    code = 'sales_return_order'


class SalesTaskPermission(ModelPermission):
    code = 'sales_task'


__all__ = [
    'SalesOrderPermission', 'SalesReturnOrderPermission', 'SalesTaskPermission',
]
