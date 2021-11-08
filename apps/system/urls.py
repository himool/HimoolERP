from extensions.routers import *
from apps.system.views import *


router = BaseRouter()
router.register('permission_types', PermissionTypeViewSet, 'permission_type')
router.register('roles', RoleViewSet, 'role')
router.register('users', UserViewSet, 'user')
router.register('user', UserActionViewSet, 'user_action')
urlpatterns = router.urls
