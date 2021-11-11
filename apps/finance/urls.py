from extensions.routers import *
from apps.purchase.views import *


router = BaseRouter()
router.register('purchase_orders', PurchaseOrderViewSet, 'purchase_order')
urlpatterns = router.urls
