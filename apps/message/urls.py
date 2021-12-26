from extensions.routers import *
from apps.message.views import *


router = BaseRouter()
router.register('inventory_messages', InventoryMessageViewSet, 'inventory_message')
urlpatterns = router.urls
