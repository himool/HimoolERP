from extensions.common.base import *
from extensions.serializers import *
from extensions.exceptions import *
from apps.system.models import *
from apps.data.models import *
from apps.goods.models import *
from apps.purchase.models import *
from apps.sales.models import *


# System
class RoleOptionSerializer(ModelSerializer):

    class Meta:
        model = Role
        fields = ['id', 'name']


class UserOptionSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'name', 'is_active']


# Data
class WarehouseOptionSerializer(ModelSerializer):

    class Meta:
        model = Warehouse
        fields = ['id', 'number', 'name', 'is_locked', 'is_active']


class ClientCategoryOptionSerializer(ModelSerializer):

    class Meta:
        model = ClientCategory
        fields = ['id', 'name']


class ClientOptionSerializer(ModelSerializer):

    class Meta:
        model = Client
        fields = ['id', 'number', 'name', 'level', 'is_active']


class SupplierCategoryOptionSerializer(ModelSerializer):

    class Meta:
        model = SupplierCategory
        fields = ['id', 'name']


class SupplierOptionSerializer(ModelSerializer):

    class Meta:
        model = Supplier
        fields = ['id', 'number', 'name', 'is_active']


class AccountOptionSerializer(ModelSerializer):

    class Meta:
        model = Account
        fields = ['id', 'number', 'name', 'is_active']


class ChargeItemOptionSerializer(ModelSerializer):

    class Meta:
        model = ChargeItem
        fields = ['id', 'name']


# Goods
class GoodsCategoryOptionSerializer(ModelSerializer):

    class Meta:
        model = GoodsCategory
        fields = ['id', 'name']


class GoodsUnitOptionSerializer(ModelSerializer):

    class Meta:
        model = GoodsUnit
        fields = ['id', 'name']


class GoodsOptionSerializer(ModelSerializer):

    class Meta:
        model = Goods
        fields = ['id', 'number', 'name', 'barcode', 'enable_batch_control', 'shelf_life_days',
                  'purchase_price', 'retail_price', 'level_price1', 'level_price2',
                  'level_price3', 'is_active']


class BatchOptionSerializer(ModelSerializer):
    unit_name = CharField(source='goods.unit.name', read_only=True, label='单位名称')

    class Meta:
        model = Batch
        fields = ['id', 'number', 'remain_quantity', 'unit_name', 'production_date', 'expiration_date']


# Purchase
class PurchaseOrderOptionSerializer(ModelSerializer):

    class PurchaseGoodsItemSerializer(ModelSerializer):
        goods_number = CharField(source='goods.number', read_only=True, label='商品编号')
        goods_name = CharField(source='goods.name', read_only=True, label='商品名称')
        goods_barcode = CharField(source='goods.barcode', read_only=True, label='商品条码')
        unit_name = CharField(source='goods.unit.name', read_only=True, label='单位名称')

        class Meta:
            model = PurchaseGoods
            fields = ['id', 'goods', 'goods_number', 'goods_name', 'goods_barcode', 'purchase_quantity',
                      'purchase_price', 'total_amount', 'return_quantity', 'unit_name']

    class PurchaseAccountItemSerializer(ModelSerializer):
        account_number = CharField(source='account.number', read_only=True, label='账户编号')
        account_name = CharField(source='account.name', read_only=True, label='账户名称')

        class Meta:
            model = PurchaseAccount
            fields = ['id', 'account', 'account_number', 'account_name', 'payment_amount']

    warehouse_number = CharField(source='warehouse.number', read_only=True, label='仓库编号')
    warehouse_name = CharField(source='warehouse.name', read_only=True, label='仓库名称')
    supplier_number = CharField(source='supplier.number', read_only=True, label='供应商编号')
    supplier_name = CharField(source='supplier.name', read_only=True, label='供应商名称')
    handler_name = CharField(source='handler.name', read_only=True, label='经手人名称')
    creator_name = CharField(source='creator.name', read_only=True, label='创建人名称')
    purchase_goods_items = PurchaseGoodsItemSerializer(
        source='purchase_goods_set', many=True, label='采购商品Item')
    purchase_account_items = PurchaseAccountItemSerializer(
        source='purchase_accounts', required=False, many=True, label='采购结算账户Item')

    class Meta:
        model = PurchaseOrder
        fields = ['id', 'number', 'warehouse', 'warehouse_number', 'warehouse_name', 'supplier',
                  'supplier_number', 'supplier_name', 'handler', 'handler_name', 'handler',
                  'handle_time', 'remark', 'total_quantity', 'other_amount', 'total_amount',
                  'payment_amount', 'arrears_amount', 'is_void', 'enable_auto_stock_in', 'creator',
                  'creator_name', 'create_time', 'purchase_goods_items', 'purchase_account_items']


# Sales
class SalesOrderOptionSerializer(ModelSerializer):

    class SalesGoodsItemSerializer(ModelSerializer):
        goods_number = CharField(source='goods.number', read_only=True, label='商品编号')
        goods_name = CharField(source='goods.name', read_only=True, label='商品名称')
        goods_barcode = CharField(source='goods.barcode', read_only=True, label='商品条码')
        unit_name = CharField(source='goods.unit.name', read_only=True, label='单位名称')

        class Meta:
            model = SalesGoods
            fields = ['id', 'goods', 'goods_number', 'goods_name', 'goods_barcode', 'sales_quantity',
                      'sales_price', 'total_amount', 'return_quantity', 'unit_name']

    class SalesAccountItemSerializer(ModelSerializer):
        account_number = CharField(source='account.number', read_only=True, label='账户编号')
        account_name = CharField(source='account.name', read_only=True, label='账户名称')

        class Meta:
            model = SalesAccount
            fields = ['id', 'account', 'account_number', 'account_name', 'collection_amount']

    warehouse_number = CharField(source='warehouse.number', read_only=True, label='仓库编号')
    warehouse_name = CharField(source='warehouse.name', read_only=True, label='仓库名称')
    client_number = CharField(source='client.number', read_only=True, label='客户编号')
    client_name = CharField(source='client.name', read_only=True, label='客户名称')
    handler_name = CharField(source='handler.name', read_only=True, label='经手人名称')
    creator_name = CharField(source='creator.name', read_only=True, label='创建人名称')
    sales_goods_items = SalesGoodsItemSerializer(
        source='sales_goods_set', many=True, label='采购商品Item')
    sales_account_items = SalesAccountItemSerializer(
        source='sales_accounts', required=False, many=True, label='采购结算账户Item')

    class Meta:
        model = SalesOrder
        fields = ['id', 'number', 'warehouse', 'warehouse_number', 'warehouse_name', 'client',
                  'client_number', 'client_name', 'handler', 'handler_name',
                  'handle_time', 'remark', 'total_quantity', 'discount', 'other_amount', 'total_amount',
                  'collection_amount', 'arrears_amount', 'is_void', 'enable_auto_stock_out', 'creator',
                  'creator_name', 'create_time', 'sales_goods_items', 'sales_account_items']


__all__ = [
    'RoleOptionSerializer', 'UserOptionSerializer',
    'WarehouseOptionSerializer',
    'ClientCategoryOptionSerializer', 'ClientOptionSerializer',
    'SupplierCategoryOptionSerializer', 'SupplierOptionSerializer',
    'AccountOptionSerializer', 'ChargeItemOptionSerializer',
    'GoodsCategoryOptionSerializer', 'GoodsUnitOptionSerializer', 'GoodsOptionSerializer',
    'BatchOptionSerializer',
    'PurchaseOrderOptionSerializer',
    'SalesOrderOptionSerializer',
]
