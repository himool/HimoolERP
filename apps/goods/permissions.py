from extensions.permissions import InterfacePermission


class GoodsPermission(InterfacePermission):
    code = 'goods'


class BatchPermission(InterfacePermission):
    code = 'batch'


class InventoryPermission(InterfacePermission):
    code = 'inventory'


__all__ = [
    'GoodsPermission', 'BatchPermission', 'InventoryPermission',
]
