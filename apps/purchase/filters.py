from django_filters import rest_framework as filters
from .models import PaymentRecord, PurchaseOrder
import pendulum


class PurchaseOrderFilter(filters.FilterSet):
    start_date = filters.CharFilter(field_name='date', lookup_expr='gte')
    end_date = filters.CharFilter(method='end_date_filter', label='end_date')

    class Meta:
        model = PurchaseOrder
        fields = ['start_date', 'end_date', 'warehouse', 'supplier', 'is_done', 'is_return']

    def end_date_filter(self, queryset, name, value):
        date = pendulum.parse(value).add(days=1)
        return queryset.filter(date__lte=date)


class PurchasePaymentRecordFilter(filters.FilterSet):
    is_return = filters.BooleanFilter(field_name='purchase_order__is_return')
    
    class Meta:
        model = PaymentRecord
        fields = ['is_return']
