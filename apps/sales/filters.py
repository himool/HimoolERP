from django_filters import rest_framework as filters
from .models import SalesOrder, SalesTask, PaymentRecord
import pendulum


class SalesOrderFilter(filters.FilterSet):
    start_date = filters.CharFilter(field_name='date', lookup_expr='gte')
    end_date = filters.CharFilter(method='end_date_filter', label='end_date')

    class Meta:
        model = SalesOrder
        fields = ['start_date', 'end_date', 'warehouse', 'is_done', 'is_return', 'client']

    def end_date_filter(self, queryset, name, value):
        date = pendulum.parse(value).add(days=1)
        return queryset.filter(date__lte=date)


class SalesTaskFilter(filters.FilterSet):
    datetime = filters.CharFilter(method='datetime_filter', label='datetime')

    class Meta:
        model = SalesTask
        fields = ['datetime']

    def datetime_filter(self, queryset, name, value):
        return queryset.filter(start_date__lte=value, end_date__gte=value)


class SalesOrderProfitFilter(filters.FilterSet):
    start_date = filters.CharFilter(field_name='date', lookup_expr='gte')
    end_date = filters.CharFilter(method='end_date_filter', label='end_date')

    class Meta:
        model = SalesOrder
        fields = ['warehouse', 'start_date', 'end_date']

    def end_date_filter(self, queryset, name, value):
        date = pendulum.parse(value).add(days=1)
        return queryset.filter(date__lte=date)


class SalesPaymentRecordFilter(filters.FilterSet):
    is_return = filters.BooleanFilter(field_name='sales_order__is_return')
    
    class Meta:
        model = PaymentRecord
        fields = ['is_return']
