import Cookies from 'js-cookie'
import axios from '@/config/request'


// Category
export function categoryList(params) {
  return axios({
    url: '/api/goods_categories/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'get',
    params,
  })
}

export function categoryCreate(form) {
  return axios({
    url: '/api/goods_categories/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'post',
    data: form,
  })
}

export function categoryUpdate(form) {
  return axios({
    url: `/api/goods_categories/${form.id}/`,
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'put',
    data: form,
  })
}

export function categoryDestroy(form) {
  return axios({
    url: `/api/goods_categories/${form.id}/`,
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

export function goodsRead(params) {
  if (params.id) {    
    return axios({
      url: `/api/goods/${params.id}/`,
      headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
      method: 'get',
    })
  }
}

export function goodsReadByCode() {
    return axios({
      url: `/api/goods/code/`,
      headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
      method: 'get',
    })
}

export function goodsReadByNumber() {
  return axios({
    url: `/api/goods/number/`,
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'get',
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
