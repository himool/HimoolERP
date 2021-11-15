from extensions.permissions import InterfacePermission


class StockTransferPermission(InterfacePermission):
    code = 'stock_transfer'


__all__ = [
    'StockTransferPermission',
]
