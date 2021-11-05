from extensions.models import *


class Warehouse(Model, ModelMixin):
    """仓库"""


class Client(Model):
    """客户"""


class Supplier(Model):
    """供应商"""


class Account(Model):
    """结算账户"""


class ChargeItem(Model):
    """收支项目"""


class ClientCategory(Model):
    """客户分类"""


class SupplierCategory(Model):
    """供应商分类"""


class GoodsCategory(Model):
    """商品分类"""


class GoodsUnit(Model):
    """商品单位"""


__all__ = [

]
