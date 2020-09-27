import Cookies from 'js-cookie'
import axios from 'axios'
import Qs from 'qs'


export function login(params) {
  return axios({
    url: '/user/login/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'post',
    data: Qs.stringify(params),
  })
}

export function logout() {
  return axios({
    url: '/user/logout/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'post',
  })
}

export function register(params) {
  return axios({
    url: '/user/register/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'post',
    data: Qs.stringify(params),
  })
}

export function getInfo() {
  return axios({
    url: '/user/get_info/',
    method: 'get',
  })
}

export function setPassword(params) {
  return axios({
    url: '/user/set_password/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'post',
    data: Qs.stringify(params),
  })
}

export function getCaptcha(params) {
  return axios({
    url: '/user/get_captcha/',
    method: 'get',
    params,
  })
}
