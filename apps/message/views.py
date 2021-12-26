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


class InventoryMessageViewSet(BaseViewSet, ListModelMixin):
    """库存预警"""

    serializer_class = InventoryMessageSerializer
    permission_classes = [IsAuthenticated, InventoryMessagePermission]
    select_related_fields = ['goods', 'goods__unit']
    queryset = Inventory.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset().filter(goods__enable_inventory_warning=True)
        queryset = queryset.filter(
            Q(goods__inventory_upper__isnull=False) & Q(total_quantity__gt=F('goods__inventory_upper')) |
            Q(goods__inventory_lower__isnull=False) & Q(total_quantity__lte=F('goods__inventory_lower'))
        )
        return queryset


__all__ = [
    'InventoryMessageViewSet',
]
