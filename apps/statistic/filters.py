from django_filters.rest_framework import FilterSet
from django_filters.filters import *
from apps.purchase.models import *


class PurchaseReportFilter(FilterSet):
    start_date = DateFilter(field_name='purchase_order__create_time', required=True, lookup_expr='gte', label='开始日期')
    end_date = DateFilter(field_name='purchase_order__create_time', required=True, lookup_expr='lt', label='结束日期')

    class Meta:
        model = PurchaseGoods
        fields = ['start_date', 'end_date']


__all__ = [
    'PurchaseReportFilter',
]
