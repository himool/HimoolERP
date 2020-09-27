from utils.permissions import BasePermission


class CategoryPermission(BasePermission):
    name = 'CATEGORY'
    view_set = ('POST', 'PUT', 'DELETE')
    permission = 'CATEGORY_POST_PUT_DELETE'


class GoodsPermission(BasePermission):
    name = 'SPECIFICATION'
    view_set = ('POST', 'PUT', 'DELETE')
