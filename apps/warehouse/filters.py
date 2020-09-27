from django_filters import rest_framework as filters
from .models import Flow, Inventory
from django.db.models import Q, F


class InventoryFilter(filters.FilterSet):
    warehouse = filters.NumberFilter(field_name='warehouse')
    category = filters.NumberFilter(field_name='goods__category')
    min_quantity = filters.NumberFilter(field_name='quantity', lookup_expr='gte')
    max_quantity = filters.NumberFilter(field_name='quantity', lookup_expr='lte')
    is_filter_zero = filters.BooleanFilter(method='is_filter_zero_filter', label='is_filter_zero')
    is_filter_negative = filters.BooleanFilter(method='is_filter_negative_filter', label='is_filter_negative')
    is_show_warning = filters.BooleanFilter(method='is_show_warning_filter', label='is_show_warning')
    search = filters.CharFilter(method='search_filter', label='search_filter')
    ordering = filters.CharFilter(method='ordering_filter', label='ordering_filter')

    class Meta:
        model = Inventory
        fields = ['warehouse', 'category', 'min_quantity', 'max_quantity', 'is_filter_zero', 'search',
                  'is_filter_negative', 'ordering', 'is_show_warning']

    def is_filter_zero_filter(self, queryset, name, value):
        return queryset.exclude(quantity=0) if value else queryset

    def is_filter_negative_filter(self, queryset, name, value):
        return queryset.filter(quantity__gte=0) if value else queryset

    def is_show_warning_filter(self, queryset, name, value):
        return queryset.filter(quantity__lte=F('goods__inventory_warning_lower_limit')) if value else queryset

    def search_filter(self, queryset, name, value):
        return queryset.filter(Q(goods__name__startswith=value) | Q(goods__code__startswith=value))

    def ordering_filter(self, queryset, name, value):
        ordering_fields = {'goods_code': 'goods__code', '-goods_code': '-goods__code', 'goods_name': 'goods__name',
                           '-goods_name': '-goods__name', 'category': 'goods__category', '-category': '-goods__category',
                           'warehouse': 'warehouse', '-warehouse': '-warehouse', 'quantity': 'quantity',
                           '-quantity': '-quantity', 'purchase_price': 'goods__purchase_price',
                           '-purchase_price': '-goods__purchase_price'}

        return queryset.order_by(ordering_fields.get(value, 'goods__code'))


class FlowFilter(filters.FilterSet):
    category = filters.NumberFilter(field_name='goods__category')

    class Meta:
        model = Flow
        fields = ['warehouse', 'type', 'category']
