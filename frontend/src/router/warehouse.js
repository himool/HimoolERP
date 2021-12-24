export default {
  path: '/warehouse',
  name: 'warehouse',
  component: () => import('@/layouts/BaseLayout'),
  redirect: '/warehouse/material_stock_in',
  children: [
    {
      path: 'material_stock_in',
      meta: { title: '原料入库', permission: 'material_stock_in' },
      component: () => import('@/views/warehouse/materialStockIn/index'),
    },
    {
      path: 'material_stock_in_create',
      meta: { title: '原料入库新增', permission: 'material_stock_in_create' },
      component: () => import('@/views/warehouse/materialStockInCreate/index'),
    },
    {
      path: 'material_stock_in_edit',
      meta: { title: '原料入库编辑', permission: 'material_stock_in_edit' },
      component: () => import('@/views/warehouse/materialStockInEdit/index'),
    },
    {
      path: 'material_stock_in_detail',
      meta: { title: '原料入库详情', permission: 'material_stock_in_detail' },
      component: () => import('@/views/warehouse/materialStockInDetail/index'),
    },
    {
      path: 'material_stock_out',
      meta: { title: '原料出库', permission: 'material_stock_out' },
      component: () => import('@/views/warehouse/materialStockOut/index'),
    },
    {
      path: 'material_stock_out_create',
      meta: { title: '原料出库新增', permission: 'material_stock_out_create' },
      component: () => import('@/views/warehouse/materialStockOutCreate/index'),
    },
    {
      path: 'material_stock_out_edit',
      meta: { title: '原料出库编辑', permission: 'material_stock_out_edit' },
      component: () => import('@/views/warehouse/materialStockOutEdit/index'),
    },
    {
      path: 'material_stock_out_detail',
      meta: { title: '原料出库详情', permission: 'material_stock_out_detail' },
      component: () => import('@/views/warehouse/materialStockOutDetail/index'),
    },
    {
      path: 'material_stock',
      meta: { title: '原料库存', permission: 'material_stock' },
      component: () => import('@/views/warehouse/materialStock/index'),
    },
    {
      path: 'material_stock_in_out_detail',
      meta: { title: '原料出入库明细', permission: 'material_stock_in_out_detail' },
      component: () => import('@/views/warehouse/materialStockInOutDetail/index'),
    },
    {
      path: 'product_stock_in',
      meta: { title: '成品入库', permission: 'product_stock_in' },
      component: () => import('@/views/warehouse/productStockIn/index'),
    },
    {
      path: 'product_stock_in_create',
      meta: { title: '成品入库新增', permission: 'product_stock_in_create' },
      component: () => import('@/views/warehouse/productStockInCreate/index'),
    },
    {
      path: 'product_stock_in_edit',
      meta: { title: '成品入库编辑', permission: 'product_stock_in_edit' },
      component: () => import('@/views/warehouse/productStockInEdit/index'),
    },
    {
      path: 'product_stock_in_detail',
      meta: { title: '成品入库详情', permission: 'product_stock_in_detail' },
      component: () => import('@/views/warehouse/productStockInDetail/index'),
    },
    {
      path: 'product_stock_out',
      meta: { title: '成品出库', permission: 'product_stock_out' },
      component: () => import('@/views/warehouse/productStockOut/index'),
    },
    {
      path: 'product_stock_out_create',
      meta: { title: '成品出库新增', permission: 'product_stock_out_create' },
      component: () => import('@/views/warehouse/productStockOutCreate/index'),
    },
    {
      path: 'product_stock_out_edit',
      meta: { title: '成品出库编辑', permission: 'product_stock_out_edit' },
      component: () => import('@/views/warehouse/productStockOutEdit/index'),
    },
    {
      path: 'product_stock_out_detail',
      meta: { title: '成品出库详情', permission: 'product_stock_out_detail' },
      component: () => import('@/views/warehouse/productStockOutDetail/index'),
    },
    {
      path: 'product_stock',
      meta: { title: '成品库存', permission: 'product_stock' },
      component: () => import('@/views/warehouse/productStock/index'),
    },
    {
      path: 'product_stock_in_out_detail',
      meta: { title: '成品出入库明细', permission: 'product_stock_in_out_detail' },
      component: () => import('@/views/warehouse/productStockInOutDetail/index'),
    },
  ],
}