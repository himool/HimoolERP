from django.contrib import admin
from apps.data.models import *


admin.site.register([Warehouse, ClientCategory, Client, SupplierCategory, Supplier,
                     Account, ChargeItem])
