from rest_framework.pagination import PageNumberPagination


class PurchaseOrderPagination(PageNumberPagination):
    page_size = 15
    page_query_param = 'page'
    max_page_size = 15


class ChangeRecordPagination(PageNumberPagination):
    page_size = 20
    page_query_param = 'page'
    max_page_size = 20


class PurchasePaymentRecordPagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'page'
    max_page_size = 10
