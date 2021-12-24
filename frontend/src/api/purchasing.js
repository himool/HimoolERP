import request from '@/utils/request';

// // 日常采购
// export function purchaseList(params) {
//   return request({ url: `/purchase_requisitions/`, method: 'get', params })
// }

// export function purchaseCreate(data) {
//   return request({ url: `/purchase_requisitions/`, method: 'post', data })
// }

// export function purchaseUpdate(data) {
//   return request({ url: `/purchase_requisitions/${data.id}/`, method: 'put', data })
// }

// export function purchaseDestroy(data) {
//   return request({ url: `/purchase_requisitions/${data.id}/`, method: 'delete', data })
// }

// export function purchaseDetail(params) {
//   return request({ url: `/purchase_requisitions/${params.id}/`, method: 'get', params })
// }

// 采购开单
export function purchaseOrderCreate(data) {
  return request({ url: `/purchase_orders/`, method: 'post', data })
}

// 采购记录
export function purchaseOrderList(params) {
  return request({ url: `/purchase_orders/`, method: 'get', params })
}

// 采购单详情
export function purchaseOrderDetail(params) {
  return request({ url: `/purchase_orders/${params.id}/`, method: 'get', params })
}

// 采购记录作废
export function purchaseOrdersVoid(data) {
  return request({ url: `/purchase_orders/${data.id}/void/`, method: 'post', data })
}

// 采购退货单
export function purchaseReturnOrderCreate(data) {
  return request({ url: `/purchase_return_orders/`, method: 'post', data })
}

// 退货记录
export function purchaseReturnOrdersList(params) {
  return request({ url: `/purchase_return_orders/`, method: 'get', params })
}

// 退货记录作废
export function purchaseReturnOrdersVoid(data) {
  return request({ url: `/purchase_return_orders/${data.id}/void/`, method: 'post', data })
}
// export function purchaseOrderUpdate(data) {
//   return request({ url: `/purchase_orders/${data.id}/`, method: 'put', data })
// }

// export function purchaseOrderDestroy(data) {
//   return request({ url: `/purchase_orders/${data.id}/`, method: 'delete', data })
// }

// export function purchaseOrderDetail(params) {
//   return request({ url: `/purchase_orders/${params.id}/`, method: 'get', params })
// }
