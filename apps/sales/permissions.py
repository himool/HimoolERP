from extensions.permissions import InterfacePermission


class SalesOrderPermission(InterfacePermission):
    code = 'sales_order'


class SalesReturnOrderPermission(InterfacePermission):
    code = 'sales_return_order'


__all__ = [
    'SalesOrderPermission', 'SalesReturnOrderPermission',
]
