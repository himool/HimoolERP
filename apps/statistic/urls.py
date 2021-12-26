from extensions.routers import *
from apps.statistic.views import *


router = BaseRouter()
router.register('purchase_reports', PurchaseReportViewSet, 'purchase_report')
router.register('sales_reports', SalesReportViewSet, 'sales_report')
urlpatterns = router.urls
