from extensions.permissions import InterfacePermission


class StockInPermission(InterfacePermission):
    code = 'stock_in'


__all__ = [
    'StockInPermission',
]
