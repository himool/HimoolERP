from extensions.common.schema import *
from extensions.common.base import *
from extensions.permissions import *
from extensions.exceptions import *
from extensions.viewsets import *
from apps.data.serializers import *
from apps.data.permissions import *
from apps.data.filters import *
from apps.data.schemas import *
from apps.data.models import *
from apps.goods.models import *


class WarehouseViewSet(ModelViewSet, DataProtectMixin):
    """仓库"""

    serializer_class = WarehouseSerializer
    permission_classes = [IsAuthenticated, WarehousePermission]
    filterset_fields = ['manager', 'is_active', 'is_locked']
    search_fields = ['number', 'name', 'remark']
    ordering_fields = ['id', 'number', 'name', 'order']
    ordering = ['order', 'number']
    select_related_fields = ['manager']
    queryset = Warehouse.objects.all()

    @transaction.atomic
    def perform_create(self, serializer):
        warehouse = serializer.save()

        # 同步库存
        Inventory.objects.bulk_create([Inventory(warehouse=warehouse, goods=goods, team=self.team)
                                       for goods in Goods.objects.filter(team=self.team)])

    @extend_schema(responses={200: NumberResponse})
    @action(detail=False, methods=['get'])
    def number(self, request, *args, **kwargs):
        """获取编号"""

        number = Warehouse.get_number(self.team)
        return Response(data={'number': number}, status=status.HTTP_200_OK)

    @extend_schema(responses={200: WarehouseSerializer})
    @action(detail=True, methods=['post'])
    def lock(self, request, *args, **kwargs):
        """锁定仓库"""

        warehouse = self.get_object()
        warehouse.is_locked = False
        warehouse.save(update_fields=['is_locked'])

        serializer = WarehouseSerializer(instance=warehouse)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @extend_schema(responses={200: WarehouseSerializer})
    @action(detail=True, methods=['post'])
    def unlock(self, request, *args, **kwargs):
        """解锁仓库"""

        warehouse = self.get_object()
        warehouse.is_locked = True
        warehouse.save(update_fields=['is_locked'])

        serializer = WarehouseSerializer(instance=warehouse)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class ClientCategoryViewSet(ModelViewSet):
    """客户分类"""

    serializer_class = ClientCategorySerializer
    permission_classes = [IsAuthenticated, ClientCategoryPermission]
    search_fields = ['name', 'remark']
    ordering_fields = ['id', 'name']
    queryset = ClientCategory.objects.all()


class ClientViewSet(ModelViewSet, DataProtectMixin):
    """客户"""

    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated, ClientPermission]
    filterset_fields = ['level', 'category', 'has_arrears', 'is_active']
    search_fields = ['number', 'name', 'contact', 'remark']
    ordering_fields = ['id', 'number', 'name', 'order']
    ordering = ['order', 'id']
    select_related_fields = ['category']
    queryset = Client.objects.all()

    @extend_schema(responses={200: NumberResponse})
    @action(detail=False, methods=['get'])
    def number(self, request, *args, **kwargs):
        """获取编号"""

        number = Client.get_number(self.team)
        return Response(data={'number': number}, status=status.HTTP_200_OK)


class SupplierCategoryViewSet(ModelViewSet):
    """供应商分类"""

    serializer_class = SupplierCategorySerializer
    permission_classes = [IsAuthenticated, SupplierCategoryPermission]
    search_fields = ['name', 'remark']
    ordering_fields = ['id', 'name']
    queryset = SupplierCategory.objects.all()


class SupplierViewSet(ModelViewSet, DataProtectMixin):
    """供应商"""

    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated, SupplierPermission]
    filterset_fields = ['category', 'has_arrears', 'is_active']
    search_fields = ['number', 'name', 'contact', 'remark']
    ordering_fields = ['id', 'number', 'name', 'order']
    ordering = ['order', 'id']
    select_related_fields = ['category']
    queryset = Supplier.objects.all()

    @extend_schema(responses={200: NumberResponse})
    @action(detail=False, methods=['get'])
    def number(self, request, *args, **kwargs):
        """获取编号"""

        number = Supplier.get_number(self.team)
        return Response(data={'number': number}, status=status.HTTP_200_OK)


class AccountViewSet(ModelViewSet, DataProtectMixin):
    """结算账户"""

    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated, AccountPermission]
    filterset_fields = ['type', 'is_active']
    search_fields = ['number', 'name', 'contact', 'remark']
    ordering_fields = ['id', 'number', 'name', 'order']
    ordering = ['order', 'id']
    queryset = Account.objects.all()

    @extend_schema(responses={200: NumberResponse})
    @action(detail=False, methods=['get'])
    def number(self, request, *args, **kwargs):
        """获取编号"""

        number = Account.get_number(self.team)
        return Response(data={'number': number}, status=status.HTTP_200_OK)


class ChargeItemViewSet(ModelViewSet):
    """收支项目"""

    serializer_class = ChargeItemSerializer
    permission_classes = [IsAuthenticated, ChargeItemPermission]
    filterset_fields = ['type']
    search_fields = ['name', 'remark']
    ordering_fields = ['id', 'name']
    queryset = ChargeItem.objects.all()


__all__ = [
    'WarehouseViewSet',
    'ClientCategoryViewSet', 'ClientViewSet',
    'SupplierCategoryViewSet', 'SupplierViewSet',
    'AccountViewSet', 'ChargeItemViewSet',
]
