from extensions.common.schema import *
from extensions.common.base import *
from extensions.permissions import *
from extensions.exceptions import *
from extensions.viewsets import *
from apps.option.serializers import *
from apps.option.permissions import *
from apps.option.filters import *
from apps.option.schemas import *
from apps.system.models import *
from apps.data.models import *
from apps.goods.models import *


# System
class RoleOptionViewSet(OptionViewSet):
    serializer_class = RoleOptionSerializer
    permission_classes = [IsAuthenticated, RoleOptionPermission]
    search_fields = ['name']
    queryset = Role.objects.all()


class UserOptionViewSet(OptionViewSet):
    serializer_class = UserOptionSerializer
    permission_classes = [IsAuthenticated, UserOptionPermission]
    search_fields = ['username', 'name']
    queryset = User.objects.filter(is_active=True)


# Data
class WarehouseOptionViewSet(OptionViewSet):
    serializer_class = WarehouseOptionSerializer
    permission_classes = [IsAuthenticated, WarehouseOptionPermission]
    filterset_fields = ['manager']
    search_fields = ['number', 'name']
    ordering_fields = ['id', 'number', 'order']
    ordering = ['order', 'number', 'id']
    queryset = Warehouse.objects.filter(is_active=True)


class ClientOptionViewSet(OptionViewSet):
    serializer_class = ClientOptionSerializer
    permission_classes = [IsAuthenticated, ClientOptionPermission]
    filterset_fields = ['level', 'category', 'has_arrears']
    search_fields = ['number', 'name']
    ordering_fields = ['id', 'number', 'order']
    ordering = ['order', 'number', 'id']
    queryset = Client.objects.filter(is_active=True)


class SupplierOptionViewSet(OptionViewSet):
    serializer_class = SupplierOptionSerializer
    permission_classes = [IsAuthenticated, SupplierOptionPermission]
    filterset_fields = ['category', 'has_arrears']
    search_fields = ['number', 'name']
    ordering_fields = ['id', 'number', 'order']
    ordering = ['order', 'number', 'id']
    queryset = Supplier.objects.filter(is_active=True)


class AccountOptionViewSet(OptionViewSet):
    serializer_class = AccountOptionSerializer
    permission_classes = [IsAuthenticated, AccountOptionPermission]
    search_fields = ['number', 'name']
    ordering_fields = ['id', 'number', 'order']
    ordering = ['order', 'number', 'id']
    queryset = Account.objects.filter(is_active=True)


class ChargeItemOptionViewSet(OptionViewSet):
    serializer_class = ChargeItemOptionSerializer
    permission_classes = [IsAuthenticated, ChargeItemOptionPermission]
    search_fields = ['name']
    queryset = ChargeItem.objects.all()


class ClientCategoryOptionViewSet(OptionViewSet):
    serializer_class = ClientCategoryOptionSerializer
    permission_classes = [IsAuthenticated, ClientCategoryOptionPermission]
    search_fields = ['name']
    queryset = ClientCategory.objects.all()


class SupplierCategoryOptionViewSet(OptionViewSet):
    serializer_class = SupplierCategoryOptionSerializer
    permission_classes = [IsAuthenticated, SupplierCategoryOptionPermission]
    search_fields = ['name']
    queryset = SupplierCategory.objects.all()


class GoodsCategoryOptionViewSet(OptionViewSet):
    serializer_class = GoodsCategoryOptionSerializer
    permission_classes = [IsAuthenticated, GoodsCategoryOptionPermission]
    search_fields = ['name']
    queryset = GoodsCategory.objects.all()


class GoodsUnitOptionViewSet(OptionViewSet):
    serializer_class = GoodsUnitOptionSerializer
    permission_classes = [IsAuthenticated, GoodsUnitOptionPermission]
    search_fields = ['name']
    queryset = GoodsUnit.objects.all()


# Goods
class GoodsOptionViewSet(OptionViewSet):
    serializer_class = GoodsOptionSerializer
    permission_classes = [IsAuthenticated, GoodsOptionPermission]
    filterset_fields = ['category']
    search_fields = ['number', 'name']
    ordering_fields = ['id', 'number', 'order']
    ordering = ['order', 'number', 'id']
    queryset = Goods.objects.filter(is_active=True)


class BatchOptionViewSet(OptionViewSet):
    serializer_class = BatchOptionSerializer
    permission_classes = [IsAuthenticated, BatchOptionPermission]
    filterset_fields = ['warehouse', 'goods']
    ordering_fields = ['id', 'number']
    ordering = ['-number', 'id']
    select_related_fields = ['goods__unit']
    queryset = Batch.objects.filter(has_stock=True)


__all__ = [
    'RoleOptionViewSet', 'UserOptionViewSet',
    'WarehouseOptionViewSet', 'ClientOptionViewSet', 'SupplierOptionViewSet', 'AccountOptionViewSet',
    'ChargeItemOptionViewSet', 'ClientCategoryOptionViewSet', 'SupplierCategoryOptionViewSet',
    'GoodsCategoryOptionViewSet', 'GoodsUnitOptionViewSet',
    'GoodsOptionViewSet', 'BatchOptionViewSet',
]
