import request from '@/utils/request';

// 我的合同
export function myContractList(params) {
  return request({ url: `/my_contract_orders/`, method: 'get', params })
}

export function myContractCreate(data) {
  return request({ url: `/my_contract_orders/`, method: 'post', data })
}

export function myContractUpdate(data) {
  return request({ url: `/my_contract_orders/${data.id}/`, method: 'put', data })
}

export function myContractDestroy(data) {
  return request({ url: `/my_contract_orders/${data.id}/`, method: 'delete', data })
}

export function myContractApply(data) {
  return request({ url: `/contract_orders/${data.id}/apply/`, method: 'post', data })
}

// 我的合同详情
export function myContractDetail(params) {
  return request({ url: `/my_contract_orders/${params.id}/`, method: 'get', params })
}

// 公司合同
export function companyContractList(params) {
  return request({ url: `/company_contract_orders/`, method: 'get', params })
}
// 公司合同详情
export function companyContractDetail(params) {
  return request({ url: `/company_contract_orders/${params.id}/`, method: 'get', params })
}

// 合同号查询
export function contractOrdersList(params) {
  return request({ url: `/contract_orders/`, method: 'get', params })
}

// 合同号查询详情
export function contractOrdersDetail(params) {
  return request({ url: `/contract_orders/${params.id}/`, method: 'get', params })
}

// 开票审批
export function approvalOrdersList(params) {
  return request({ url: `/approval_contract_orders/`, method: 'get', params })
}

// 审批
export function updateInvoicing(data) {
  return request({ url: `/contract_orders/${data.id}/invoicing/`, method: 'post', data })
}

// 开票审批留档
export function retentionOrdersList(params) {
  return request({ url: `/retention_contract_orders/`, method: 'get', params })
}

// 开票审批留档详情
export function retentionOrdersDetail(params) {
  return request({ url: `/retention_contract_orders//${params.id}/`, method: 'get', params })
}