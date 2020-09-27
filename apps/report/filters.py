from django_filters import rest_framework as filters
from purchase.models import PurchaseGoods, PurchaseOrder
from sales.models import SalesGoods, SalesOrder
from django.db.models import Q, F
import pendulum


class PurcahseReportFilter(filters.FilterSet):
    category = filters.NumberFilter(field_name='goods__category')
    start_date = filters.CharFilter(field_name='purchase_order__date', lookup_expr='gte')
    end_date = filters.CharFilter(method='end_date_filter', label='end_date')

    class Meta:
        model = PurchaseGoods
        fields = ['category', 'start_date', 'end_date']

    def end_date_filter(self, queryset, name, value):
        date = pendulum.parse(value).add(days=1)
        return queryset.filter(purchase_order__date__lte=date)


class SalesReportFilter(filters.FilterSet):
    category = filters.NumberFilter(field_name='goods__category')
    start_date = filters.CharFilter(field_name='sales_order__date', lookup_expr='gte')
    end_date = filters.CharFilter(method='end_date_filter', label='end_date')

    class Meta:
        model = SalesGoods
        fields = ['category', 'start_date', 'end_date']

    def end_date_filter(self, queryset, name, value):
        date = pendulum.parse(value).add(days=1)
        return queryset.filter(sales_order__date__lte=date)


class FinancialReportFilter(filters.FilterSet):
    start_date = filters.CharFilter(field_name='sales_order__date', lookup_expr='gte')
    end_date = filters.CharFilter(method='end_date_filter', label='end_date')

    class Meta:
        model = SalesGoods
        fields = ['start_date', 'end_date']

    def end_date_filter(self, queryset, name, value):
        date = pendulum.parse(value).add(days=1)
        return queryset.filter(sales_order__date__lte=date)


class PurchaseStatisticsFilter(filters.FilterSet):
    start_date = filters.CharFilter(field_name='date', lookup_expr='gte')
    end_date = filters.CharFilter(method='end_date_filter', label='end_date')

    class Meta:
        model = PurchaseOrder
        fields = ['start_date', 'end_date', 'supplier']

    def end_date_filter(self, queryset, name, value):
        date = pendulum.parse(value).add(days=1)
        return queryset.filter(date__lte=date)


class SalesStatisticsFilter(filters.FilterSet):
    start_date = filters.CharFilter(field_name='date', lookup_expr='gte')
    end_date = filters.CharFilter(method='end_date_filter', label='end_date')

    class Meta:
        model = SalesOrder
        fields = ['start_date', 'end_date', 'client']

    def end_date_filter(self, queryset, name, value):
        date = pendulum.parse(value).add(days=1)
        return queryset.filter(date__lte=date)
