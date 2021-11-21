export const goodsOptions1 = [
  { label: '规格管理', value: 'SPECIFICATION_POST_PUT_DELETE' },
  { label: '分类管理', value: 'CATEGORY_POST_PUT_DELETE' },
  { label: '仓库管理', value: 'WAREHOUSE_POST_PUT_DELETE' },
  { label: '供应商管理', value: 'SUPPLIER_POST_PUT_DELETE' },
]

export const goodsOptions2 = [
  { label: '编辑商品', value: 'GOODS_PUT' },
  { label: '删除商品', value: 'GOODE_DELETE' },
  { label: '添加商品', value: 'GOODS_POST' },
  { label: '查看采购价', value: 'PURCHASE_PRICE_GET' },
]

export const purchaseOptions = [
  { label: '查看采购单', value: 'PURCHASE_GET' },
  { label: '提交采购单/草稿', value: 'PURCHASE_POST' },
  { label: '修改草稿', value: 'PURCHASE_PUT' },
  { label: '删除草稿/撤销采购单', value: 'PURCHASE_DELETE' },
]

export const salesOptions = [
  { label: '查看销售单', value: 'SALES_GET' },
  { label: '开销售单', value: 'SALES_POST' },
  { label: '撤销销售单', value: 'SALES_DELETE' },
  { label: '修改销售员', value: 'CHANGE_SELLER' },
]

export const warehouseOptions1 = [
  { label: '库存状况', value: 'WAREHOUSE_STATUS_GET' },
  { label: '查看库存流水', value: 'WAREHOUSE_FLOW_GET' },
]

export const warehouseOptions2 = [
  { label: '查看调拨单', value: 'REQUISITION_GET' },
  { label: '提交调拨单/保存调拨草稿', value: 'REQUISITION_POST' },
  { label: '修改草稿', value: 'REQUISITION_UPDATE' },
  { label: '删除草稿/撤销调拨单', value: 'REQUISITION_DELETE' },
]

export const warehouseOptions3 = [
  { label: '查看盘点单', value: 'COUNTING_GET' },
  { label: '提交盘点单/保存盘点草稿', value: 'COUNTING_CREATE' },
  { label: '修改草稿', value: 'COUNTING_UPDATE' },
  { label: '删除草稿', value: 'COUNTING_DELETE' },
]

export const reportOptions = [
  { label: '查看销售报表', value: 'SALES_REPORT_GET' },
  { label: '查看销售毛利', value: 'SALES_GROSS_PROFIT_GET' },
  { label: '查看采购报表', value: 'PURCHASE_REPORT_GET' },
]

export const accountOptions = [
  { label: '管理子帐号', value: 'SUBUSER_POST_PUT_DELETE' },
  { label: '创建角色', value: 'ROLE_POST' },
  { label: '编辑角色', value: 'ROLE_PUT' },
  { label: '删除角色', value: 'ROLE_DELETE' },
]