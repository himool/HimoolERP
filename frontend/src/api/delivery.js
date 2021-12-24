import request from '@/utils/request';

// 装箱清单
export function packingList(params) {
  return request({ url: `/packing_orders/`, method: 'get', params })
}

export function packingCreate(data) {
  return request({ url: `/packing_orders/`, method: 'post', data })
}

export function packingUpdate(data) {
  return request({ url: `/packing_orders/${data.id}/`, method: 'put', data })
}

export function packingDestroy(data) {
  return request({ url: `/packing_orders/${data.id}/`, method: 'delete', data })
}

export function packingDetail(params) {
  return request({ url: `/packing_orders/${params.id}/`, method: 'get', params })
}
