from extensions.permissions import ModelPermission


class InventoryWarningPermission(ModelPermission):
    code = 'inventory_warning'


__all__ = [
    'InventoryWarningPermission',
]
