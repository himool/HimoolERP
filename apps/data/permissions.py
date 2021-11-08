from extensions.permissions import InterfacePermission


class WarehousePermission(InterfacePermission):
    code = 'warehouse'


class ClientPermission(InterfacePermission):
    code = 'client'


class SupplierPermission(InterfacePermission):
    code = 'supplier'


class AccountPermission(InterfacePermission):
    code = 'account'


class ChargeItemPermission(InterfacePermission):
    code = 'charge_item'


class ClientCategoryPermission(InterfacePermission):
    code = 'client_category'


class SupplierCategoryPermission(InterfacePermission):
    code = 'supplier_category'


class GoodsCategoryPermission(InterfacePermission):
    code = 'goods_category'


class GoodsUnitPermission(InterfacePermission):
    code = 'goods_unit'


__all__ = [
    'WarehousePermission', 'ClientPermission', 'SupplierPermission', 'AccountPermission',
    'ChargeItemPermission', 'ClientCategoryPermission', 'SupplierCategoryPermission',
    'GoodsCategoryPermission', 'GoodsUnitPermission',
]
