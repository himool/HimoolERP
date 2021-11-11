from extensions.permissions import *
from extensions.exceptions import *
from extensions.viewsets import *
from apps.purchase.serializers import *
from apps.purchase.permissions import *
from apps.purchase.filters import *
from apps.purchase.schemas import *
from apps.purchase.models import *


class PurchaseOrderViewSet(BaseViewSet, ListModelMixin, RetrieveModelMixin, CreateModelMixin):
    """采购单据"""

    serializer_class = PurchaseOrderSerializer
    permission_classes = [IsAuthenticated, PurchaseOrderPermission]
    filterset_class = PurchaseOrderFilter
    search_fields = ['number', 'supplier__number', 'supplier__name', 'remark']
    ordering_fields = ['id', 'number', 'total_quantity', 'total_amount', 'create_time']
    ordering = ['-number', 'id']
    select_related_fields = ['warehouse', 'supplier', 'handler', 'creator']
    prefetch_related_fields = ['purchase_goods_set', 'purchase_goods_set__goods__unit',
                               'payment_order__payment_accounts']
    queryset = PurchaseOrder.objects.all()

    @extend_schema(responses={200: NumberResponse})
    @action(detail=False, methods=['get'])
    def number(self, request, *args, **kwargs):
        """获取编号"""

        number = PurchaseOrder.get_number(self.team)
        return Response(data={'number': number}, status=status.HTTP_200_OK)


__all__ = [
    'PurchaseOrderViewSet',
]
