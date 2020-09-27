from rest_framework.pagination import PageNumberPagination


class PurchaseReportPagination(PageNumberPagination):
    page_size = 20
    page_query_param = 'page'
    max_page_size = 20


class SalesReportPagination(PageNumberPagination):
    page_size = 20
    page_query_param = 'page'
    max_page_size = 20
