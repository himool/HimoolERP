import Cookies from 'js-cookie'
import axios from 'axios'

// Warehouse
export function warehouseList() {
  return axios({
    url: '/api/warehouse/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'get',
  })
}

export function warehouseCreate(form) {
  return axios({
    url: '/api/warehouse/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'post',
    data: form,
  })
}

export function warehouseUpdate(form) {
  return axios({
    url: `/api/warehouse/${form.id}/`,
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'put',
    data: form,
  })
}

export function warehouseDestroy(form) {
  return axios({
    url: `/api/warehouse/${form.id}/`,
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'delete',
  })
}

// Inventory
export function inventoryList(params) {
  return axios({
    url: '/api/inventory/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'get',
    params,
  })
}

export function exportInventory(params) {
  return axios({
    url: '/api/inventory/export/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'get',
    params,
  })
}

// Flow
export function flowList(params) {
  return axios({
    url: '/api/flows/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'get',
    params,
  })
}

// CountingList
export function countingListList() {
  return axios({
    url: '/api/counting_list/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'get',
  })
}

export function countingListCreate(form) {
  return axios({
    url: '/api/counting_list/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'post',
    data: form,
  })
}

export function countingListRetrieve(params) {
  return axios({
    url: `/api/counting_list/${params.id}/`,
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'get',
  })
}

// Requisition
export function requisitionList(params) {
  return axios({
    url: '/api/requisition/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'get',
    params,
  })
}

export function requisitionCreate(form) {
  return axios({
    url: '/api/requisition/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'post',
    data: form,
  })
}

export function requisitionRetrieve(params) {
  return axios({
    url: `/api/requisition/${params.id}/`,
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'get',
  })
}
