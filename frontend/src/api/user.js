import Cookies from 'js-cookie'
import axios from '@/config/request'
import Qs from 'qs'

export function login(params) {
  return axios({
    url: '/api/user/login/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'post',
    data: Qs.stringify(params),
  })
}

export function userList(params) {
  return axios({
    url: '/api/users/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'get',
    params,
  })
}

export function logout() {
  return axios({
    url: '/api/user/logout/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'post',
  })
}

export function setPassword(data) {
  return axios({
    url: '/api/user/set_password/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'post',
    data,
  })
}

export function getInfo() {
  return axios({
    url: '/api/user/get_info/',
    method: 'get',
  })
}

// Config
export function configRetrieve() {
  return axios({
    url: '/api/user/configs/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'get',
  })
}

export function configUpdate(data) {
  return axios({
    url: '/api/user/configs/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'put',
    data,
  })
}

export function getRoles() {
  return axios({
    url: '/api/roles/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'get',
  })
}