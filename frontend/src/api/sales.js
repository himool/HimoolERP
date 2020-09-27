import Cookies from 'js-cookie'
import axios from 'axios'

// SalesOrder
export function salesOrderList(params) {
  return axios({
    url: '/api/sales_order/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'get',
    params,
  })
}

export function salesOrderCreate(form) {
  return axios({
    url: '/api/sales_order/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'post',
    data: form,
  })
}

export function salesOrderRetrieve(params) {
  return axios({
    url: `/api/sales_order/${params.id}/`,
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'get',
  })
}

export function salesOrderConfirm(form) {
  return axios({
    url: `/api/sales_order/confirm/`,
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'post',
    data: form,
  })
}

export function salesOrderDestroy(form) {
  return axios({
    url: `/api/sales_order/${form.id}/`,
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'delete',
  })
}

// SalesTask
export function salesTaskList(params) {
  return axios({
    url: '/api/sales_tasks/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'get',
    params,
  })
}

export function salesTaskCreate(form) {
  return axios({
    url: '/api/sales_tasks/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'post',
    data: form,
  })
}

// salesOrderProfit
export function salesOrderProfitList(params) {
  return axios({
    url: '/api/sales_order_profit/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'get',
    params,
  })
}

export function salesOrderProfitUpdate(form) {
  return axios({
    url: `/api/sales_order_profit/${form.id}/`,
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'put',
    data: form,
  })
}

export function salesOrderTotalProfit(params) {
  return axios({
    url: '/api/sales_order_profit/total_profit/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'get',
    params,
  })
}

// SalesValue
export function salesValueList(params) {
  return axios({
    url: '/api/sales_values/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'get',
    params,
  })
}

// SalesTopTen
export function salesTopTenList(params) {
  return axios({
    url: '/api/sales_top_ten/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'get',
    params,
  })
}

// Client
export function clientList(params) {
  return axios({
    url: '/api/clients/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'get',
    params,
  })
}

export function clientCreate(form) {
  return axios({
    url: '/api/clients/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'post',
    data: form,
  })
}

export function clientDestroy(form) {
  return axios({
    url: `/api/clients/${form.id}/`,
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'delete',
  })
}

// SalesPaymentRecord
export function salesPaymentRecord(params) {
  return axios({
    url: '/api/sales_payment_records/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'get',
    params,
  })
}

// PaymentRecord
export function paymentRecordCreate(form) {
  return axios({
    url: `/api/sales_order/payment/`,
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'post',
    data: form,
  })
}