import Cookies from 'js-cookie'
import axios from '@/config/request'

// Supplier
export function supplierList(params) {
  return axios({
    url: '/api/supplier/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'get',
    params,
  })
}

export function supplierCreate(form) {
  return axios({
    url: '/api/supplier/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'post',
    data: form,
  })
}

export function supplierUpdate(form) {
  return axios({
    url: `/api/supplier/${form.id}/`,
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'put',
    data: form,
  })
}

export function supplierDestroy(form) {
  return axios({
    url: `/api/supplier/${form.id}/`,
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'delete',
  })
}

// PurchaseOrder
export function purchaseOrderList(params) {
  return axios({
    url: '/api/purchase_order/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'get',
    params,
  })
}

export function purchaseOrderCreate(form) {
  return axios({
    url: '/api/purchase_order/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'post',
    data: form,
  })
}

export function purchaseOrderRetrieve(params) {
  return axios({
    url: `/api/purchase_order/${params.id}/`,
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'get',
  })
}

export function purchaseOrderConfirm(form) {
  return axios({
    url: `/api/purchase_order/confirm/`,
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'post',
    data: form,
  })
}

export function purchaseOrderDestroy(form) {
  return axios({
    url: `/api/purchase_order/${form.id}/`,
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'delete',
  })
}

// PurchasePriceChangeRecord
export function changeRecordList() {
  return axios({
    url: '/api/change_records/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'get',
  })
}

// PurchasePaymentRecord
export function purchasePaymentRecord(params) {
  return axios({
    url: '/api/purchase_payment_records/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'get',
    params,
  })
}

// PaymentRecord
export function paymentRecordCreate(form) {
  return axios({
    url: `/api/purchase_order/payment/`,
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'post',
    data: form,
  })
}