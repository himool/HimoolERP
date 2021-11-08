from django.contrib import admin
from apps.data.models import *


admin.register([Warehouse, Client, Supplier, Account,
                ChargeItem, ClientCategory, SupplierCategory, GoodsCategory, GoodsUnit])
