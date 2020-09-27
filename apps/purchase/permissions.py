from utils.permissions import BasePermission


class SupplierPermission(BasePermission):
    name = 'SUPPLIER'
    view_set = ('POST', 'PUT', 'DELETE')
    permission = 'SUPPLIER_POST_PUT_DELETE'


class PurchaseOrderPermission(BasePermission):
    name = 'PURCHASE'
    view_set = ('GET', 'POST', 'PUT', 'DELETE')
