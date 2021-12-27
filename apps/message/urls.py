from extensions.routers import *
from apps.message.views import *


router = BaseRouter()
router.register('inventory_warnings', InventoryWarningViewSet, 'inventory_warning')
router.register('sales_task_reminders', SalesTaskReminderViewSet, 'sales_task_reminder')
urlpatterns = router.urls
