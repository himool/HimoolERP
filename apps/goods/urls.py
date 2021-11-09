from extensions.routers import *
from apps.goods.views import *


router = BaseRouter()
router.register('goods', GoodsViewSet, 'goods')
router.register('batchs', BatchViewSet, 'batch')
router.register('inventories', InventoryViewSet, 'inventory')
urlpatterns = router.urls
