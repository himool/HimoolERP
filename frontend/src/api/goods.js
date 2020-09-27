import Cookies from 'js-cookie'
import axios from 'axios'


// Category
export function categoryList() {
  return axios({
    url: '/api/categories/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'get',
  })
}

export function categoryCreate(form) {
  return axios({
    url: '/api/categories/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'post',
    data: form,
  })
}

export function categoryUpdate(form) {
  return axios({
    url: `/api/categories/${form.id}/`,
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'put',
    data: form,
  })
}

export function categoryDestroy(form) {
  return axios({
    url: `/api/categories/${form.id}/`,
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'delete',
  })
}

// Goods
export function goodsList(params) {
  return axios({
    url: '/api/goods/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'get',
    params,
  })
}

export function goodsCreate(form) {
  return axios({
    url: '/api/goods/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'post',
    data: form,
  })
}

export function goodsUpdate(form) {
  return axios({
    url: `/api/goods/${form.id}/`,
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'put',
    data: form,
  })
}

export function goodsDestroy(form) {
  return axios({
    url: `/api/goods/${form.id}/`,
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'delete',
  })
}
