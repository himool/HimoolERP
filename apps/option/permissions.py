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
GoodsCategoryOptionPermission = BasePermission
GoodsUnitOptionPermission = BasePermission

# Goods
GoodsOptionPermission = BasePermission
BatchOptionPermission = BasePermission


__all__ = [
    'RoleOptionPermission', 'UserOptionPermission',
    'WarehouseOptionPermission', 'ClientOptionPermission', 'SupplierOptionPermission', 'AccountOptionPermission',
    'ChargeItemOptionPermission', 'ClientCategoryOptionPermission', 'SupplierCategoryOptionPermission',
    'GoodsCategoryOptionPermission', 'GoodsUnitOptionPermission',
    'GoodsOptionPermission', 'BatchOptionPermission',
]
