from rest_framework.pagination import PageNumberPagination


class BasePagination(PageNumberPagination):
    invalid_page_message = '无效页面'
    page_size_query_param = 'page_size'
    max_page_size = 64
    page_size = 16


class OptionPagination(BasePagination):
    max_page_size = 999999
    page_size = 16


__all__ = [
    'BasePagination', 'OptionPagination',
]
