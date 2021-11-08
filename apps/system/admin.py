from django.contrib import admin
from apps.system.models import *


admin.register([Team, PermissionType, Permission, Role, User])
