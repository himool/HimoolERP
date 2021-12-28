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
from apps.sales.models import *
from apps.finance.models import *


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
                                           'purchase_order__warehouse', 'purchase_order__supplier',
                                           'purchase_order__creator')
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


class SalesReportViewSet(BaseViewSet):
    """销售报表"""

    permission_classes = [IsAuthenticated, SalesReportPermission]
    filterset_class = SalesReportFilter
    search_fields = ['goods__number', 'goods__name']
    queryset = SalesGoods.objects.all()

    @extend_schema(parameters=[SalesReportParameter],
                   responses={200: SalesReportStatisticResponse})
    @action(detail=False, methods=['get'])
    def statistics(self, request, *args, **kwargs):
        """统计"""

        queryset = self.filter_queryset(self.get_queryset())
        result = queryset.aggregate(
            total_count=Count('sales_order', distinct=True),
            total_quantity=Coalesce(Sum('sales_quantity'), Value(0.0)),
            total_amount=Coalesce(Sum('total_amount'), Value(0, output_field=AmountField()))
        )

        return Response(data=result, status=status.HTTP_200_OK)

    @extend_schema(parameters=[SalesReportParameter],
                   responses={200: SalesReportDetialSerializer})
    @action(detail=False, methods=['get'])
    def detials(self, request, *args, **kwargs):
        """明细"""

        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.select_related('goods', 'goods__category', 'goods__unit', 'sales_order',
                                           'sales_order__warehouse', 'sales_order__supplier',
                                           'sales_order__creator')
        queryset = self.paginate_queryset(queryset)

        serializer = SalesReportDetialSerializer(instance=queryset, many=True)
        return self.get_paginated_response(serializer.data)

    @extend_schema(parameters=[SalesReportParameter],
                   responses={200: SalesReportGroupByGoodsResponse})
    @action(detail=False, methods=['get'])
    def group_by_goods(self, request, *args, **kwargs):
        """商品汇总"""

        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.select_related('goods', 'goods__category', 'goods__unit')
        queryset = queryset.values('goods').annotate(
            goods_number=F('goods__number'), goods_name=F('goods__name'),
            goods_barcode=F('goods__barcode'), goods_spec=F('goods__spec'),
            category_name=F('goods__category__name'), unit_name=F('goods__unit__name'),
            total_sales_quantity=Coalesce(Sum('sales_quantity'), Value(0.0)),
            total_sales_amount=Coalesce(Sum('total_amount'), Value(0, output_field=AmountField())),
            min_sales_price=Min('sales_price'), avg_sales_price=Avg('sales_price'),
            max_sales_price=Max('sales_price')
        )
        queryset = self.paginate_queryset(queryset)

        return self.get_paginated_response(queryset)


class SalesHotGoodsViewSet(BaseViewSet, ListModelMixin):
    """销售前十商品"""

    permission_classes = [IsAuthenticated, SalesHotGoodsPermission]
    pagination_class = None
    filterset_class = SalesHotGoodsFilter
    queryset = SalesGoods.objects.all()

    @extend_schema(parameters=[SalesHotGoodsParameter], responses={200: SalesHotGoodsResponse})
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.select_related('goods', 'goods__category', 'goods__unit')
        queryset = queryset.values('goods').annotate(
            goods_number=F('goods__number'), goods_name=F('goods__name'),
            goods_barcode=F('goods__barcode'), goods_spec=F('goods__spec'),
            category_name=F('goods__category__name'), unit_name=F('goods__unit__name'),
            total_sales_quantity=Coalesce(Sum('sales_quantity'), Value(0.0)),
        ).order_by('-total_sales_quantity')[:10]

        return Response(data=queryset, status=status.HTTP_200_OK)


class SalesTrendViewSet(BaseViewSet, ListModelMixin):
    """销售走势"""

    permission_classes = [IsAuthenticated, SalesTrendPermission]
    pagination_class = None
    filterset_class = SalesTrendFilter
    queryset = SalesOrder.objects.all()

    @extend_schema(parameters=[SalesTrendParameter], responses={200: SalesTrendResponse})
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.select_related('warehouse')
        queryset = queryset.extra(select={'date': connection.ops.date_trunc_sql('day', 'create_time')})
        queryset = queryset.values('warehouse', 'date').annotate(
            warehouse_number=F('warehouse__number'), warehouse_name=F('warehouse__name'),
            total_sales_amount=Coalesce(Sum('total_amount'), Value(0, output_field=AmountField())),
        )

        return Response(data=queryset, status=status.HTTP_200_OK)


class ProfitTrendViewSet(BaseViewSet, ListModelMixin):
    """利润走势"""

    permission_classes = [IsAuthenticated, ProfitTrendPermission]
    pagination_class = None
    filterset_class = ProfitTrendFilter
    queryset = SalesGoods.objects.all()

    @extend_schema(parameters=[ProfitTrendParameter], responses={200: ProfitTrendResponse})
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.select_related('sales_order__warehouse')
        queryset = queryset.extra(select={'date': connection.ops.date_trunc_sql('day', 'create_time')})
        queryset = queryset.values('sales_order__warehouse', 'date').annotate(
            warehouse=F('sales_order__warehouse'),
            warehouse_number=F('sales_order__warehouse__number'),
            warehouse_name=F('sales_order__warehouse__name'),
            total_profit_amount=Coalesce(Sum(
                F('total_amount') - F('sales_quantity') * F('goods__purchase_price'),
                output_field=AmountField()), Value(0, output_field=AmountField())),
        ).values('warehouse', 'warehouse_number', 'warehouse_name', 'total_profit_amount', 'date')

        return Response(data=queryset, status=status.HTTP_200_OK)


class FinanceStatisticViewSet(FunctionViewSet):
    """收支统计"""

    def list(self, request, *args, **kwargs):
        PaymentOrder.objects.filter().values('number', 'create_time', 'total_amount', suppliser_)

        return Response()

    

__all__ = [
    'PurchaseReportViewSet', 'SalesReportViewSet',
    'SalesHotGoodsViewSet', 'SalesTrendViewSet', 'ProfitTrendViewSet',
    'FinanceStatisticViewSet',
]
