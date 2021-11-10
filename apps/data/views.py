from extensions.permissions import *
from extensions.exceptions import *
from extensions.viewsets import *
from apps.data.serializers import *
from apps.data.permissions import *
from apps.data.filters import *
from apps.data.schemas import *
from apps.data.models import *
from apps.goods.models import *


class WarehouseViewSet(BaseViewSet, ReadWriteMixin):
    """仓库"""

    serializer_class = WarehouseSerializer
    permission_classes = [IsAuthenticated, WarehousePermission]
    filterset_fields = ['manager', 'is_active', 'is_locked']
    search_fields = ['number', 'name', 'remark']
    ordering_fields = ['id', 'number', 'name', 'order']
    ordering = ['order', 'id']
    select_related_fields = ['manager']
    queryset = Warehouse.objects.all()

    @transaction.atomic
    def perform_create(self, serializer):
        warehouse = serializer.save()

        # 同步库存
        Inventory.objects.bulk_create([Inventory(warehouse=warehouse, goods=goods, team=self.team)
                                       for goods in Goods.objects.filter(team=self.team)])

    def perform_destroy(self, instance):
        try:
            instance.delete()
        except ProtectedError:
            raise ValidationError(f'仓库[{instance.name}]已被引用, 无法删除')

    @extend_schema(responses={200: NumberResponse})
    @action(detail=False, methods=['get'])
    def number(self, request, *args, **kwargs):
        """获取编号"""

        instance = Warehouse.objects.filter(team=self.team).last()
        try:
            result = re.match('^(.*?)([1-9]+)$', instance.number)
            number = result.group(1) + str(int(result.group(2)) + 1)
        except AttributeError:
            number = 'W001'

        return Response(data={'number': number}, status=status.HTTP_200_OK)


class ClientViewSet(BaseViewSet, ReadWriteMixin):
    """客户"""

    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated, ClientPermission]
    filterset_fields = ['level', 'category', 'has_arrears', 'is_active']
    search_fields = ['number', 'name', 'contact', 'remark']
    ordering_fields = ['id', 'number', 'name', 'order']
    ordering = ['order', 'id']
    select_related_fields = ['category']
    queryset = Client.objects.all()

    def perform_destroy(self, instance):
        try:
            instance.delete()
        except ProtectedError:
            raise ValidationError(f'客户[{instance.name}]已被引用, 无法删除')

    @extend_schema(responses={200: NumberResponse})
    @action(detail=False, methods=['get'])
    def number(self, request, *args, **kwargs):
        """获取编号"""

        instance = Client.objects.filter(team=self.team).last()
        try:
            result = re.match('^(.*?)([1-9]+)$', instance.number)
            number = result.group(1) + str(int(result.group(2)) + 1)
        except AttributeError:
            number = 'C001'

        return Response(data={'number': number}, status=status.HTTP_200_OK)


class SupplierViewSet(BaseViewSet, ReadWriteMixin):
    """供应商"""

    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated, SupplierPermission]
    filterset_fields = ['category', 'has_arrears', 'is_active']
    search_fields = ['number', 'name', 'contact', 'remark']
    ordering_fields = ['id', 'number', 'name', 'order']
    ordering = ['order', 'id']
    select_related_fields = ['category']
    queryset = Supplier.objects.all()

    def perform_destroy(self, instance):
        try:
            instance.delete()
        except ProtectedError:
            raise ValidationError(f'供应商[{instance.name}]已被引用, 无法删除')

    @extend_schema(responses={200: NumberResponse})
    @action(detail=False, methods=['get'])
    def number(self, request, *args, **kwargs):
        """获取编号"""

        instance = Supplier.objects.filter(team=self.team).last()
        try:
            result = re.match('^(.*?)([1-9]+)$', instance.number)
            number = result.group(1) + str(int(result.group(2)) + 1)
        except AttributeError:
            number = 'S001'

        return Response(data={'number': number}, status=status.HTTP_200_OK)


class AccountViewSet(BaseViewSet, ReadWriteMixin):
    """结算账户"""

    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated, AccountPermission]
    filterset_fields = ['type', 'is_active']
    search_fields = ['number', 'name', 'contact', 'remark']
    ordering_fields = ['id', 'number', 'name', 'order']
    ordering = ['order', 'id']
    queryset = Account.objects.all()

    def perform_destroy(self, instance):
        try:
            instance.delete()
        except ProtectedError:
            raise ValidationError(f'结算账户[{instance.name}]已被引用, 无法删除')

    @extend_schema(responses={200: NumberResponse})
    @action(detail=False, methods=['get'])
    def number(self, request, *args, **kwargs):
        """获取编号"""

        instance = Account.objects.filter(team=self.team).last()
        try:
            result = re.match('^(.*?)([1-9]+)$', instance.number)
            number = result.group(1) + str(int(result.group(2)) + 1)
        except AttributeError:
            number = 'A001'

        return Response(data={'number': number}, status=status.HTTP_200_OK)


class ChargeItemViewSet(BaseViewSet, ReadWriteMixin):
    """收支项目"""

    serializer_class = ChargeItemSerializer
    permission_classes = [IsAuthenticated, ChargeItemPermission]
    filterset_fields = ['type']
    search_fields = ['name', 'remark']
    ordering_fields = ['id', 'name']
    queryset = ChargeItem.objects.all()


class ClientCategoryViewSet(BaseViewSet, ReadWriteMixin):
    """客户分类"""

    serializer_class = ClientCategorySerializer
    permission_classes = [IsAuthenticated, ClientCategoryPermission]
    search_fields = ['name', 'remark']
    ordering_fields = ['id', 'name']
    queryset = ClientCategory.objects.all()


class SupplierCategoryViewSet(BaseViewSet, ReadWriteMixin):
    """供应商分类"""

    serializer_class = SupplierCategorySerializer
    permission_classes = [IsAuthenticated, SupplierCategoryPermission]
    search_fields = ['name', 'remark']
    ordering_fields = ['id', 'name']
    queryset = SupplierCategory.objects.all()


class GoodsCategoryViewSet(BaseViewSet, ReadWriteMixin):
    """商品分类"""

    serializer_class = GoodsCategorySerializer
    permission_classes = [IsAuthenticated, GoodsCategoryPermission]
    search_fields = ['name', 'remark']
    ordering_fields = ['id', 'name']
    queryset = GoodsCategory.objects.all()


class GoodsUnitViewSet(BaseViewSet, ReadWriteMixin):
    """商品单位"""

    serializer_class = GoodsUnitSerializer
    permission_classes = [IsAuthenticated, GoodsUnitPermission]
    search_fields = ['name', 'remark']
    ordering_fields = ['id', 'name']
    queryset = GoodsUnit.objects.all()


__all__ = [
    'WarehouseViewSet', 'ClientViewSet', 'SupplierViewSet', 'AccountViewSet',
    'ChargeItemViewSet', 'ClientCategoryViewSet', 'SupplierCategoryViewSet',
    'GoodsCategoryViewSet', 'GoodsUnitViewSet',
]
