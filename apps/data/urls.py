from extensions.routers import *
from apps.data.views import *


router = BaseRouter()
router.register('warehouses', WarehouseViewSet, 'role')
router.register('clients', ClientViewSet, 'role')
router.register('suppliers', SupplierViewSet, 'role')
router.register('accounts', AccountViewSet, 'role')
router.register('charge_items', ChargeItemViewSet, 'role')
router.register('client_categories', ClientCategoryViewSet, 'role')
router.register('supplier_categories', SupplierCategoryViewSet, 'role')
router.register('goods_categories', GoodsCategoryViewSet, 'role')
router.register('goods_units', GoodsUnitViewSet, 'role')
urlpatterns = router.urls
