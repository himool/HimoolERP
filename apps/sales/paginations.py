from rest_framework.pagination import PageNumberPagination


class SalesOrderPagination(PageNumberPagination):
    page_size = 15
    page_query_param = 'page'
    max_page_size = 15


class SalesTaskPagination(PageNumberPagination):
    page_size = 20
    page_query_param = 'page'
    max_page_size = 20


class SalesOrderProfitPagination(PageNumberPagination):
    page_size = 5
    page_query_param = 'page'
    max_page_size = 5


class SalesProfitPagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'page'
    max_page_size = 10


class ClientPagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'page'
    max_page_size = 10


class SalesPaymentRecordPagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'page'
    max_page_size = 10
