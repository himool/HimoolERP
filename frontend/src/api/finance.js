import request from '@/utils/request';

// 打款记录
export function paymentList(params) {
  return request({ url: `/payment_records/`, method: 'get', params })
}

export function paymentCreate(data) {
  return request({ url: `/payment_records/`, method: 'post', data })
}

export function paymentUpdate(data) {
  return request({ url: `/payment_records/${data.id}/`, method: 'put', data })
}

export function paymentDestroy(data) {
  return request({ url: `/payment_records/${data.id}/`, method: 'delete', data })
}

// 采购对账单
export function purchaseStatementsList(params) {
  return request({ url: `/purchase_statements/`, method: 'get', params })
}

// 往来记录
export function collectionList(params) {
  return request({ url: `/collection_records/`, method: 'get', params })
}

export function collectionCreate(data) {
  return request({ url: `/collection_records/`, method: 'post', data })
}

export function collectionUpdate(data) {
  return request({ url: `/collection_records/${data.id}/`, method: 'put', data })
}

export function collectionDestroy(data) {
  return request({ url: `/collection_records/${data.id}/`, method: 'delete', data })
}

// 销售对账单
export function salesStatementssList(params) {
  return request({ url: `/sales_statements/`, method: 'get', params })
}