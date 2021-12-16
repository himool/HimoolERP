from extensions.routers import *
from apps.data.views import *


router = BaseRouter()
router.register('warehouses', WarehouseViewSet, 'warehouse')
router.register('client_categories', ClientCategoryViewSet, 'client_category')
router.register('clients', ClientViewSet, 'client')
router.register('supplier_categories', SupplierCategoryViewSet, 'supplier_category')
router.register('suppliers', SupplierViewSet, 'supplier')
router.register('accounts', AccountViewSet, 'account')
router.register('charge_items', ChargeItemViewSet, 'charge_item')
urlpatterns = router.urls
