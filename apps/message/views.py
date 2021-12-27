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
from apps.sales.models import *
from apps.stock_in.models import *
from apps.stock_out.models import *


class InventoryWarningViewSet(BaseViewSet, ListModelMixin):
    """库存预警"""

    permission_classes = [IsAuthenticated, InventoryWarningPermission]
    queryset = Inventory.objects.all()

    @extend_schema(responses={200: InventoryWarningResponse})
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        queryset = queryset.filter(goods__enable_inventory_warning=True, goods__is_active=True)
        queryset = queryset.select_related('goods', 'goods__unit')
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


class SalesTaskReminderViewSet(BaseViewSet, ListModelMixin):
    """销售任务提醒"""

    serializer_class = SalesTaskReminderSerializer
    permission_classes = [IsAuthenticated]
    select_related_fields = ['warehouse', 'goods', 'goods__unit']
    queryset = SalesTask.objects.all()

    def get_queryset(self):
        now_time = pendulum.now()
        return super().get_queryset().filter(start_time__lte=now_time, end_time__gt=now_time,
                                             salesperson=self.user, is_completed=False)


class StockInOrderReminderViewSet(BaseViewSet, ListModelMixin):
    """入库任务提醒"""

    serializer_class = StockInOrderReminderSerializer
    permission_classes = [IsAuthenticated, StockInReminderPermission]
    select_related_fields = ['warehouse']
    queryset = StockInOrder.objects.all()

    def get_queryset(self):
        return super().get_queryset().filter(is_completed=False, is_void=False)


class StockOutOrderReminderViewSet(BaseViewSet, ListModelMixin):
    """出库任务提醒"""

    serializer_class = StockOutOrderReminderSerializer
    permission_classes = [IsAuthenticated, StockOutReminderPermission]
    select_related_fields = ['warehouse']
    queryset = StockOutOrder.objects.all()

    def get_queryset(self):
        return super().get_queryset().filter(is_completed=False, is_void=False)


__all__ = [
    'InventoryWarningViewSet', 'SalesTaskReminderViewSet',
    'StockInOrderReminderViewSet', 'StockOutOrderReminderViewSet',
]
