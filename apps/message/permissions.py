from extensions.permissions import ModelPermission


class InventoryMessagePermission(ModelPermission):
    code = 'inventory_message'


__all__ = [
    'InventoryMessagePermission',
]
