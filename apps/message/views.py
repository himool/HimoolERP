from extensions.common.schema import *
from extensions.common.base import *
from extensions.permissions import *
from extensions.exceptions import *
from extensions.viewsets import *
from extensions.models import *
from apps.message.serializers import *
from apps.message.permissions import *
from apps.message.filters import *
from apps.message.schemas import *
from apps.message.models import *
from apps.goods.models import *


class InventoryWarningViewSet(BaseViewSet, ListModelMixin):
    """库存预警"""

    permission_classes = [IsAuthenticated, InventoryWarningPermission]
    queryset = Inventory.objects.all()

    @extend_schema(responses={200: InventoryWarningResponse})
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        queryset = queryset.filter(goods__enable_inventory_warning=True, goods__is_active=True)
        queryset = queryset.values('goods').annotate(
            goods_number=F('goods__number'), goods_name=F('goods__name'),
            goods_barcode=F('goods__barcode'), unit_name=F('goods__unit__name'),
            inventory_upper=F('goods__inventory_upper'), inventory_lower=F('goods__inventory_lower'),
            total_quantity=Sum('total_quantity'),
        )
        queryset = queryset.filter(
            Q(goods__inventory_upper__isnull=False) &
            Q(total_quantity__gt=F('goods__inventory_upper')) |
            Q(goods__inventory_lower__isnull=False) &
            Q(total_quantity__lte=F('goods__inventory_lower'))
        )
        queryset = self.paginate_queryset(queryset)

        return self.get_paginated_response(queryset)


__all__ = [
    'InventoryWarningViewSet',
]
