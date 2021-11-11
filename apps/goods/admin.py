from django.contrib import admin
from apps.goods.models import *


admin.site.register([Goods, Batch, Inventory])
