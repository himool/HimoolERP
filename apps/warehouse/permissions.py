from utils.permissions import BasePermission


class WarehousePermission(BasePermission):
    name = 'WAREHOUSE'
    view_set = ('POST', 'PUT', 'DELETE')
    permission = 'WAREHOUSE_POST_PUT_DELETE'


class InventoryPermission(BasePermission):
    name = 'INVENTORY'
    view_set = ('GET',)
    permission = 'WAREHOUSE_STATUS_GET'


class FlowPermission(BasePermission):
    name = 'FLOW'
    view_set = ('GET',)
    permission = 'WAREHOUSE_FLOW_GET'


class CountingListPermission(BasePermission):
    name = 'COUNTING'
    view_set = ('GET', 'POST', 'PUT', 'DELETE')


class RequisitionPermission(BasePermission):
    name = 'REQUISITION'
    view_set = ('GET', 'POST', 'PUT', 'DELETE')
