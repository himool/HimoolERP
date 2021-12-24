export default [
  {
    key: '2', name: '基础数据', icon: 'table', submenus: [
      { key: '/basicData/client_classification', name: '客户分类'},
      { key: '/basicData/client', name: '客户'},
      { key: '/basicData/supplier_classification', name: '供应商分类'},
      { key: '/basicData/supplier', name: '供应商'},
      { key: '/basicData/warehouse', name: '仓库'},
      { key: '/basicData/settlement_account', name: '结算账户'},
      { key: '/basicData/revenue_expenditure_items', name: '收支项目'},
    ]
  },
  {
    key: '3', name: '商品管理', icon: 'shopping', submenus: [
      { key: '/goods/classification', name: '商品分类' },
      { key: '/goods/unit', name: '商品单位' },
      { key: '/goods/information', name: '商品信息' },
    ]
  },
  {
    key: '4', name: '采购管理', icon: 'shopping-cart', submenus: [
      { key: '/purchasing/purchase_create', name: '采购开单' },
      { key: '/purchasing/purchase_record', name: '采购记录' },
      { key: '/purchasing/purchase_return_create', name: '采购退货' },
      { key: '/purchasing/return_record', name: '退货记录' },
    ]
  },
  {
    key: '8', name: '系统管理', icon: 'team', submenus: [
      { key: '/role', name: '角色管理' },
      { key: '/account', name: '员工账号' },
      { key: '/config', name: '系统配置' },
    ]
  },
]