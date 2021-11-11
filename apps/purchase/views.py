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
    select_related_fields = ['warehouse', 'supplier', 'handler', 'creator',
                             'purchase_goods_set__goods__unit']
    prefetch_related_fields = ['purchase_goods_set', 'payment_order__payment_accounts']
    queryset = PurchaseOrder.objects.all()


__all__ = [
    'PurchaseOrderViewSet',
]
