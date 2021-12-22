from extensions.permissions import BasePermission
from apps.system.permissions import *
from apps.data.permissions import *
from apps.goods.permissions import *


# System
RoleOptionPermission = BasePermission
UserOptionPermission = BasePermission

# Data
WarehouseOptionPermission = BasePermission
ClientOptionPermission = BasePermission
SupplierOptionPermission = BasePermission
AccountOptionPermission = BasePermission
ChargeItemOptionPermission = BasePermission
ClientCategoryOptionPermission = BasePermission
SupplierCategoryOptionPermission = BasePermission

# Goods
GoodsCategoryOptionPermission = BasePermission
GoodsUnitOptionPermission = BasePermission
GoodsOptionPermission = BasePermission
BatchOptionPermission = BasePermission
InventoryOptionPermission = BasePermission

# Purchase
PurchaseOrderOptionPermission = BasePermission

# Sales
SalesOrderOptionPermission = BasePermission


__all__ = [
    'RoleOptionPermission', 'UserOptionPermission',
    'WarehouseOptionPermission', 'ClientOptionPermission', 'SupplierOptionPermission', 'AccountOptionPermission',
    'ChargeItemOptionPermission', 'ClientCategoryOptionPermission', 'SupplierCategoryOptionPermission',
    'GoodsCategoryOptionPermission', 'GoodsUnitOptionPermission', 'GoodsOptionPermission',
    'BatchOptionPermission', 'InventoryOptionPermission',
    'PurchaseOrderOptionPermission',
    'SalesOrderOptionPermission',
]
