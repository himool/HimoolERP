from extensions.common.schema import *
from extensions.common.base import *
from extensions.permissions import *
from extensions.exceptions import *
from extensions.viewsets import *
from extensions.models import *
from apps.statistic.serializers import *
from apps.statistic.permissions import *
from apps.statistic.filters import *
from apps.statistic.schemas import *
from apps.statistic.models import *
from apps.purchase.models import *


class PurchaseReportViewSet(BaseViewSet):
    """采购报表"""

    permission_classes = [IsAuthenticated, PurchaseReportPermission]
    filterset_class = PurchaseReportFilter
    search_fields = ['goods__number', 'goods__name']
    queryset = PurchaseGoods.objects.all()

    @extend_schema(parameters=[PurchaseReportParameter],
                   responses={200: PurchaseReportStatisticResponse})
    @action(detail=False, methods=['get'])
    def statistics(self, request, *args, **kwargs):
        """统计"""

        queryset = self.filter_queryset(self.get_queryset())
        result = queryset.aggregate(
            total_count=Count('purchase_order', distinct=True),
            total_quantity=Coalesce(Sum('purchase_quantity'), Value(0.0)),
            total_amount=Coalesce(Sum('total_amount'), Value(0, output_field=AmountField()))
        )

        return Response(data=result, status=status.HTTP_200_OK)

    @extend_schema(parameters=[PurchaseReportParameter],
                   responses={200: PurchaseReportDetialSerializer})
    @action(detail=False, methods=['get'])
    def detials(self, request, *args, **kwargs):
        """明细"""

        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.select_related('goods', 'goods__category', 'goods__unit', 'purchase_order',
                                           'purchase_order__supplier')
        queryset = self.paginate_queryset(queryset)

        serializer = PurchaseReportDetialSerializer(instance=queryset, many=True)
        return self.get_paginated_response(serializer.data)

    @extend_schema(parameters=[PurchaseReportParameter],
                   responses={200: PurchaseReportGroupByGoodsResponse})
    @action(detail=False, methods=['get'])
    def group_by_goods(self, request, *args, **kwargs):
        """商品汇总"""

        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.select_related('goods', 'goods__category', 'goods__unit')
        queryset = queryset.values('goods').annotate(
            goods_number=F('goods__number'), goods_name=F('goods__name'),
            goods_barcode=F('goods__barcode'), goods_spec=F('goods__spec'),
            category_name=F('goods__category__name'), unit_name=F('goods__unit__name'),
            total_purchase_quantity=Coalesce(Sum('purchase_quantity'), Value(0.0)),
            total_purchase_amount=Coalesce(Sum('total_amount'), Value(0, output_field=AmountField())),
            min_purchase_price=Min('purchase_price'), avg_purchase_price=Avg('purchase_price'),
            max_purchase_price=Max('purchase_price')
        )
        queryset = self.paginate_queryset(queryset)

        return self.get_paginated_response(queryset)


__all__ = [
    'PurchaseReportViewSet',
]
