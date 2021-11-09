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
    queryset = Goods.objects.all()

    @transaction.atomic
    def perform_create(self, serializer):
        goods = serializer.save()

        # 同步库存
        Inventory.objects.bulk_create([Inventory(warehouse=warehouse, goods=goods, team=self.team)
                                       for warehouse in Warehouse.objects.filter(team=self.team)])

    def perform_destroy(self, instance):
        try:
            instance.delete()
        except ProtectedError:
            raise ValidationError(f'商品[{instance.name}]已被引用, 无法删除')

    @extend_schema(responses={200: NumberResponse})
    @action(detail=False, methods=['get'])
    def number(self, request, *args, **kwargs):
        """获取编号"""

        instance = Goods.objects.filter(team=self.team).last()
        try:
            result = re.match('^(.*?)([1-9]+)$', instance.number)
            number = result.group(1) + str(int(result.group(2)) + 1)
        except AttributeError:
            number = 'G000000000001'

        return Response(data={'number': number}, status=status.HTTP_200_OK)


class BatchViewSet(BaseViewSet, ReadOnlyMixin):
    """批次"""

    serializer_class = BatchSerializer
    permission_classes = [IsAuthenticated, BatchPermission]
    filterset_fields = ['number', 'warehouse', 'goods', 'is_empty']
    search_fields = ['number', 'goods__number', 'goods__name']
    ordering_fields = ['id', 'number', 'total_quantity', 'remain_quantity', 'production_date',
                       'expiration_date', 'create_time']
    select_related_fields = ['warehouse', 'goods', 'goods__unit']
    queryset = Batch.objects.all()


class InventoryViewSet(BaseViewSet, ReadOnlyMixin):
    """库存"""

    serializer_class = InventorySerializer
    permission_classes = [IsAuthenticated, InventoryPermission]
    filterset_fields = ['warehouse', 'goods', 'is_empty']
    search_fields = ['goods__number', 'goods__name']
    ordering_fields = ['id', 'total_quantity']
    select_related_fields = ['warehouse', 'goods', 'goods__unit']
    queryset = Inventory.objects.all()


__all__ = [
    'GoodsViewSet', 'BatchViewSet', 'InventoryViewSet',
]
