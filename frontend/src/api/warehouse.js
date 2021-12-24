import request from '@/utils/request';

// 原料入库
export function materialStockInList(params) {
  return request({ url: `/material_stock_in_orders/`, method: 'get', params })
}

export function materialStockInCreate(data) {
  return request({ url: `/material_stock_in_orders/`, method: 'post', data })
}

export function materialStockInUpdate(data) {
  return request({ url: `/material_stock_in_orders/${data.id}/`, method: 'put', data })
}

export function materialStockInDestroy(data) {
  return request({ url: `/material_stock_in_orders/${data.id}/`, method: 'delete', data })
}

export function materialStockInDetail(params) {
  return request({ url: `/material_stock_in_orders/${params.id}/`, method: 'get', params })
}

export function materialStockInConfirm(data) {
  return request({ url: `/material_stock_in_orders/${data.id}/confirm/`, method: 'post', data })
}

// 原料出库
export function materialStockOutList(params) {
  return request({ url: `/material_stock_out_orders/`, method: 'get', params })
}

export function materialStockOutCreate(data) {
  return request({ url: `/material_stock_out_orders/`, method: 'post', data })
}

export function materialStockOutUpdate(data) {
  return request({ url: `/material_stock_out_orders/${data.id}/`, method: 'put', data })
}

export function materialStockOutDestroy(data) {
  return request({ url: `/material_stock_out_orders/${data.id}/`, method: 'delete', data })
}

export function materialStockOutDetail(params) {
  return request({ url: `/material_stock_out_orders/${params.id}/`, method: 'get', params })
}

export function materialStockOutConfirm(data) {
  return request({ url: `/material_stock_out_orders/${data.id}/confirm/`, method: 'post', data })
}

// 原料库存
export function materialInventoriesList(params) {
  return request({ url: `/material_inventories/`, method: 'get', params })
}

// 原料出入库明细
export function materialInventoryFlowsList(params) {
  return request({ url: `/material_inventory_flows/`, method: 'get', params })
}

// 成品入库
export function productStockInList(params) {
  return request({ url: `/product_stock_in_orders/`, method: 'get', params })
}

export function productStockInCreate(data) {
  return request({ url: `/product_stock_in_orders/`, method: 'post', data })
}

export function productStockInUpdate(data) {
  return request({ url: `/product_stock_in_orders/${data.id}/`, method: 'put', data })
}

export function productStockInDestroy(data) {
  return request({ url: `/product_stock_in_orders/${data.id}/`, method: 'delete', data })
}

export function productStockInDetail(params) {
  return request({ url: `/product_stock_in_orders/${params.id}/`, method: 'get', params })
}

export function productStockInConfirm(data) {
  return request({ url: `/product_stock_in_orders/${data.id}/confirm/`, method: 'post', data })
}

// 成品出库
export function productStockOutList(params) {
  return request({ url: `/product_stock_out_orders/`, method: 'get', params })
}

export function productStockOutCreate(data) {
  return request({ url: `/product_stock_out_orders/`, method: 'post', data })
}

export function productStockOutUpdate(data) {
  return request({ url: `/product_stock_out_orders/${data.id}/`, method: 'put', data })
}

export function productStockOutDestroy(data) {
  return request({ url: `/product_stock_out_orders/${data.id}/`, method: 'delete', data })
}

export function productStockOutDetail(params) {
  return request({ url: `/product_stock_out_orders/${params.id}/`, method: 'get', params })
}

export function productStockOutConfirm(data) {
  return request({ url: `/product_stock_out_orders/${data.id}/confirm/`, method: 'post', data })
}

// 成品库存
export function productInventoriesList(params) {
  return request({ url: `/product_inventories/`, method: 'get', params })
}

// 成品出入库明细
export function productInventoryFlowsList(params) {
  return request({ url: `/product_inventory_flows/`, method: 'get', params })
}