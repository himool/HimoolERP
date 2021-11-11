from django.contrib import admin
from apps.system.models import *


admin.site.register([Team, PermissionType, Permission, Role, User])
