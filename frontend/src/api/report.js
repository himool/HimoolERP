import Cookies from 'js-cookie'
import axios from '@/config/request'

// PurchaseReport
export function purchaseReportList(params) {
  return axios({
    url: '/api/purchase_orders/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'get',
    params,
  })
}

// SalesReport
export function salesReportList(params) {
  return axios({
    url: '/api/sales_reports/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'get',
    params,
  })
}

// FinancialReport
export function financialReportList(params) {
  return axios({
    url: '/api/financial_reports/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'get',
    params,
  })
}

// FinancialStatistics
export function financialStatistics(params) {
  return axios({
    url: '/api/financial_statistics/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'get',
    params,
  })
}

// PurchaseStatistics
export function purchaseStatistics(params) {
  return axios({
    url: '/api/purchase_statistics/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'get',
    params,
  })
}

// SalesStatistics
export function salesStatistics(params) {
  return axios({
    url: '/api/sales_statistics/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'get',
    params,
  })
}
