from extensions.permissions import InterfacePermission


class StockOutPermission(InterfacePermission):
    code = 'stock_out'


__all__ = [
    'StockOutPermission',
]
