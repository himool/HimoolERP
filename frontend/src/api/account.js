import Cookies from 'js-cookie'
import axios from 'axios'

// Role
export function roleList() {
  return axios({
    url: '/api/roles/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'get',
  })
}

export function roleCreate(form) {
  return axios({
    url: '/api/roles/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'post',
    data: form,
  })
}

export function roleUpdate(form) {
  return axios({
    url: `/api/roles/${form.id}/`,
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'put',
    data: form,
  })
}

export function roleDestroy(form) {
  return axios({
    url: `/api/roles/${form.id}/`,
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'delete',
  })
}

// Subuser
export function subuserList() {
  return axios({
    url: '/api/subusers/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'get',
  })
}

export function subuserCreate(form) {
  return axios({
    url: '/api/subusers/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'post',
    data: form,
  })
}

export function subuserUpdate(username, form) {
  return axios({
    url: `/api/subusers/${username}/`,
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'put',
    data: form,
  })
}

export function subuserReset(form) {
  return axios({
    url: `/api/subusers/${form.username}/`,
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'patch',
    data: form,
  })
}

export function subuserDestroy(form) {
  return axios({
    url: `/api/subusers/${form.username}/`,
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'delete',
  })
}


// Account
export function accountList() {
  return axios({
    url: '/api/accounts/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'get',
  })
}

export function accountCreate(form) {
  return axios({
    url: '/api/accounts/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'post',
    data: form,
  })
}

export function accountUpdate(form) {
  return axios({
    url: `/api/accounts/${form.id}/`,
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'put',
    data: form,
  })
}

export function accountDestroy(form) {
  return axios({
    url: `/api/accounts/${form.id}/`,
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'delete',
  })
}

// Seller
export function sellertList() {
  return axios({
    url: '/api/sellers/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'get',
  })
}

// Bookkeeping
export function bookkeepingList() {
  return axios({
    url: '/api/bookkeeping/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'get',
  })
}

export function bookkeepingCreate(form) {
  return axios({
    url: '/api/bookkeeping/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'post',
    data: form,
  })
}

export function bookkeepingDestroy(form) {
  return axios({
    url: `/api/bookkeeping/${form.id}/`,
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'delete',
  })
}

// StatisticalAccount
export function statisticalAccountList(params) {
  return axios({
    url: '/api/statistical_account/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'get',
    params,
  })
}

// User 
export function userList() {
  return axios({
    url: '/api/users/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'get',
  })
}