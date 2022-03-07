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
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = PurchaseReportFilter
    search_fields = ['goods__number', 'goods__name']
    queryset = PurchaseGoods.objects.all()

    def get_queryset(self):
        return super().get_queryset().filter(purchase_order__is_void=False)

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
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = SalesReportFilter
    search_fields = ['goods__number', 'goods__name']
    queryset = SalesGoods.objects.all()

    def get_queryset(self):
        return super().get_queryset().filter(sales_order__is_void=False)

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
                                           'sales_order__warehouse', 'sales_order__client',
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
    filter_backends = [DjangoFilterBackend]
    filterset_class = SalesHotGoodsFilter
    queryset = SalesGoods.objects.all()

    def get_queryset(self):
        return super().get_queryset().filter(sales_order__is_void=False)

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
    filter_backends = [DjangoFilterBackend]
    filterset_class = SalesTrendFilter
    queryset = SalesOrder.objects.all()

    def get_queryset(self):
        return super().get_queryset().filter(is_void=False)

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


class FinanceStatisticViewSet(FunctionViewSet):
    """收支统计"""

    @extend_schema(parameters=[FinanceStatisticParameter], responses={200: FinanceStatisticResponse})
    def list(self, request, *args, **kwargs):
        serializer = FinanceStatisticParameter(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        query_filters = (
            Q(create_time__gte=serializer.data['start_date']) &
            Q(create_time__lt=serializer.data['end_date']) &
            Q(is_void=False) & Q(team=self.team)
        )

        result = {}
        result |= SalesOrder.objects.filter(query_filters).aggregate(
            total_sales_amount=Coalesce(Sum('total_amount'), Value(0, output_field=AmountField())))
        result |= SalesReturnOrder.objects.filter(query_filters).aggregate(
            total_sales_reutrn_amount=Coalesce(Sum('total_amount'), Value(0, output_field=AmountField())))
        result |= PurchaseOrder.objects.filter(query_filters).aggregate(
            total_purchase_amount=Coalesce(Sum('total_amount'), Value(0, output_field=AmountField())))
        result |= PurchaseReturnOrder.objects.filter(query_filters).aggregate(
            total_purchase_return_amount=Coalesce(Sum('total_amount'), Value(0, output_field=AmountField())))
        result |= ChargeOrder.objects.filter(query_filters).filter(type=ChargeOrder.Type.INCOME).aggregate(
            total_income_amount=Coalesce(Sum('total_amount'), Value(0, output_field=AmountField())))
        result |= ChargeOrder.objects.filter(query_filters).filter(type=ChargeOrder.Type.EXPENDITURE).aggregate(
            total_expenditure_amount=Coalesce(Sum('total_amount'), Value(0, output_field=AmountField())))

        return Response(data=result, status=status.HTTP_200_OK)


class PaymentOrderDetialViewSet(BaseViewSet, ListModelMixin):
    """付款明细"""

    serializer_class = PaymentOrderDetialSerializer
    permission_classes = [IsAuthenticated, FinanceStatisticPermission]
    filter_backends = [DjangoFilterBackend]
    filterset_class = PaymentOrderDetialFilter
    queryset = PaymentOrder.objects.all()

    def get_queryset(self):
        return super().get_queryset().filter(is_void=False)


class CollectionOrderDetialViewSet(BaseViewSet, ListModelMixin):
    """收款明细"""

    serializer_class = CollectionOrderDetialSerializer
    permission_classes = [IsAuthenticated, FinanceStatisticPermission]
    filter_backends = [DjangoFilterBackend]
    filterset_class = CollectionOrderDetialFilter
    queryset = CollectionOrder.objects.all()

    def get_queryset(self):
        return super().get_queryset().filter(is_void=False)


class IncomeChargeOrderDetialViewSet(BaseViewSet, ListModelMixin):
    """收入费用明细"""

    serializer_class = IncomeChargeOrderDetialSerializer
    permission_classes = [IsAuthenticated, FinanceStatisticPermission]
    filter_backends = [DjangoFilterBackend]
    filterset_class = IncomeChargeOrderDetialFilter
    queryset = ChargeOrder.objects.all()

    def get_queryset(self):
        return super().get_queryset().filter(type=ChargeOrder.Type.INCOME, is_void=False)


class ExpenditureChargeOrderDetialViewSet(BaseViewSet, ListModelMixin):
    """支出费用明细"""

    serializer_class = ExpenditureChargeOrderDetialSerializer
    permission_classes = [IsAuthenticated, FinanceStatisticPermission]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ExpenditureChargeOrderDetialFilter
    queryset = ChargeOrder.objects.all()

    def get_queryset(self):
        return super().get_queryset().filter(type=ChargeOrder.Type.EXPENDITURE, is_void=False)


class PurchasePaymentDetialViewSet(BaseViewSet, ListModelMixin):
    """采购付款明细"""

    serializer_class = PurchasePaymentDetialSerializer
    permission_classes = [IsAuthenticated, FinanceStatisticPermission]
    filter_backends = [DjangoFilterBackend]
    filterset_class = PurchasePaymentDetialFilter
    queryset = PurchaseOrder.objects.all()

    def get_queryset(self):
        return super().get_queryset().filter(is_void=False)


class PurchaseReturnCollectionDetialViewSet(BaseViewSet, ListModelMixin):
    """采购退货收款明细"""

    serializer_class = PurchaseReturnCollectionDetialSerializer
    permission_classes = [IsAuthenticated, FinanceStatisticPermission]
    filter_backends = [DjangoFilterBackend]
    filterset_class = PurchaseReturnCollectionDetialFilter
    queryset = PurchaseReturnOrder.objects.all()

    def get_queryset(self):
        return super().get_queryset().filter(is_void=False)


class SalesCollectionDetialViewSet(BaseViewSet, ListModelMixin):
    """销售收款明细"""

    serializer_class = SalesCollectionDetialSerializer
    permission_classes = [IsAuthenticated, FinanceStatisticPermission]
    filter_backends = [DjangoFilterBackend]
    filterset_class = SalesCollectionDetialFilter
    queryset = SalesOrder.objects.all()

    def get_queryset(self):
        return super().get_queryset().filter(is_void=False)


class SalesReturnPaymentDetialViewSet(BaseViewSet, ListModelMixin):
    """销售退货付款明细"""

    serializer_class = SalesReturnPaymentDetialSerializer
    permission_classes = [IsAuthenticated, FinanceStatisticPermission]
    filter_backends = [DjangoFilterBackend]
    filterset_class = SalesReturnPaymentDetialFilter
    queryset = SalesReturnOrder.objects.all()

    def get_queryset(self):
        return super().get_queryset().filter(is_void=False)


__all__ = [
    'PurchaseReportViewSet', 'SalesReportViewSet', 'SalesHotGoodsViewSet',
    'SalesTrendViewSet', 'FinanceStatisticViewSet',
    'PaymentOrderDetialViewSet', 'CollectionOrderDetialViewSet',
    'IncomeChargeOrderDetialViewSet', 'ExpenditureChargeOrderDetialViewSet',
    'PurchasePaymentDetialViewSet', 'PurchaseReturnCollectionDetialViewSet',
    'SalesCollectionDetialViewSet', 'SalesReturnPaymentDetialViewSet',
]
