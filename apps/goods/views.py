from extensions.permissions import *
from extensions.exceptions import *
from extensions.viewsets import *
from apps.goods.serializers import *
from apps.goods.permissions import *
from apps.goods.filters import *
from apps.goods.schemas import *
from apps.goods.models import *
from apps.data.models import *


class GoodsViewSet(BaseViewSet, ReadWriteMixin):
    """商品"""

    serializer_class = GoodsSerializer
    permission_classes = [IsAuthenticated, GoodsPermission]
    filterset_fields = ['number', 'category', 'is_active']
    search_fields = ['number', 'name', 'remark']
    ordering_fields = ['id', 'number', 'name', 'order']
    ordering = ['order', 'id']
    select_related_fields = ['category', 'unit']
    prefetch_related_fields = ['inventories', 'inventories__batchs']
    queryset = Goods.objects.all()

    def perform_destroy(self, instance):
        try:
            instance.delete()
        except ProtectedError:
            raise ValidationError(f'商品[{instance.name}]已被引用, 无法删除')

    @extend_schema(responses={200: NumberResponse})
    @action(detail=False, methods=['get'])
    def number(self, request, *args, **kwargs):
        """获取编号"""

        number = Goods.get_number(self.team)
        return Response(data={'number': number}, status=status.HTTP_200_OK)


class BatchViewSet(BaseViewSet, ReadOnlyMixin):
    """批次"""

    serializer_class = BatchSerializer
    permission_classes = [IsAuthenticated, BatchPermission]
    filterset_fields = ['number', 'warehouse', 'goods', 'has_stock']
    search_fields = ['number', 'goods__number', 'goods__name']
    ordering_fields = ['id', 'number', 'total_quantity', 'remain_quantity', 'production_date',
                       'expiration_date', 'create_time']
    select_related_fields = ['warehouse', 'goods', 'goods__unit']
    queryset = Batch.objects.all()


class InventoryViewSet(BaseViewSet, ReadOnlyMixin):
    """库存"""

    serializer_class = InventorySerializer
    permission_classes = [IsAuthenticated, InventoryPermission]
    filterset_fields = ['warehouse', 'goods', 'has_stock']
    search_fields = ['goods__number', 'goods__name']
    ordering_fields = ['id', 'total_quantity']
    select_related_fields = ['warehouse', 'goods', 'goods__unit']
    queryset = Inventory.objects.all()


__all__ = [
    'GoodsViewSet', 'BatchViewSet', 'InventoryViewSet',
]
