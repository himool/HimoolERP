from extensions.routers import *
from apps.statistic.views import *


router = BaseRouter()
router.register('purchase_reports', PurchaseReportViewSet, 'purchase_report')
router.register('sales_reports', SalesReportViewSet, 'sales_report')
router.register('sales_hot_goods', SalesHotGoodsViewSet, 'sales_hot_goods')
router.register('sales_trends', SalesTrendViewSet, 'sales_trend')
router.register('profit_trends', ProfitTrendViewSet, 'profit_trend')
urlpatterns = router.urls
