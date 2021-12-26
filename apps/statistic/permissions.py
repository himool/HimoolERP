from extensions.permissions import ModelPermission


class PurchaseReportPermission(ModelPermission):
    code = 'purchase_report'


class SalesReportPermission(ModelPermission):
    code = 'sales_report'


__all__ = [
    'PurchaseReportPermission', 'SalesReportPermission',
]
