from extensions.permissions import InterfacePermission


class PurchaseOrderPermission(InterfacePermission):
    code = 'purchase_order'


class PurchaseReturnOrderPermission(InterfacePermission):
    code = 'purchase_return_order'


__all__ = [
    'PurchaseOrderPermission', 'PurchaseReturnOrderPermission',
]
