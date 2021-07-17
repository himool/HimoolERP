import Cookies from 'js-cookie'
import axios from 'axios'
import Qs from 'qs'


export function login(params) {
  return axios({
    url: '/api/user/login/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'post',
    data: Qs.stringify(params),
  })
}

export function logout() {
  return axios({
    url: '/api/user/logout/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'post',
  })
}

export function register(params) {
  return axios({
    url: '/api/user/register/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'post',
    data: Qs.stringify(params),
  })
}

export function getInfo() {
  return axios({
    url: '/api/user/get_info/',
    method: 'get',
  })
}