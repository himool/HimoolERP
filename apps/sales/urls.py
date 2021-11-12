from extensions.routers import *
from apps.sales.views import *


router = BaseRouter()
router.register('sales_orders', SalesOrderViewSet, 'sales_order')
urlpatterns = router.urls
