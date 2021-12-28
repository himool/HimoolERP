import request from '@/utils/request';

// 销售报表
export function salesReportStatistics(params) {
  return request({ url: `/sales_reports/statistics/`, method: 'get', params })
}
// 销售报表明细
export function salesReportDetialsList(params) {
  return request({ url: `/sales_reports/detials/`, method: 'get', params })
}
// 销售报表按商品汇总
export function salesReportByGoodsList(params) {
  return request({ url: `/sales_reports/group_by_goods/`, method: 'get', params })
}

// 采购报表
export function purchaseReportStatistics(params) {
  return request({ url: `/purchase_reports/statistics/`, method: 'get', params })
}
// 采购报表明细
export function purchaseReportDetialsList(params) {
  return request({ url: `/purchase_reports/detials/`, method: 'get', params })
}
// 采购报表按商品汇总
export function purchaseReportByGoodsList(params) {
  return request({ url: `/purchase_reports/group_by_goods/`, method: 'get', params })
}

// 库存报表
export function inventoryReportList(params) {
  return request({ url: `/inventories/`, method: 'get', params })
}

// 批次报表
export function batchsReportList(params) {
  return request({ url: `/batchs/`, method: 'get', params })
}

// 利润走势
export function profitTrends(params) {
  return request({ url: `/profit_trends/`, method: 'get', params })
}
