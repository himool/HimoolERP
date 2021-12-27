from extensions.routers import *
from apps.message.views import *


router = BaseRouter()
router.register('inventory_warnings', InventoryWarningViewSet, 'inventory_warning')
urlpatterns = router.urls
