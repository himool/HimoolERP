from django.contrib import admin
from apps.goods.models import *


admin.register([Goods, Batch, Inventory])
