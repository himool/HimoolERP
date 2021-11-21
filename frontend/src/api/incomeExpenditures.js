import Cookies from 'js-cookie'
import axios from '@/config/request'

 function paramsSerializer(params) {
  var result = '';
  if (params) {        
    for (const key in params) {
      result += `${key}=${params[key]}&`;
    }
    result = result.substring(0, result.length -1 )
  }
  return result;
}

// incomeExpenditures
export function incomeExpendituresList(params) {
  return axios({
    url: '/api/income_expenditures/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'get',
    params,
    paramsSerializer,
  })
}

export function incomeExpendituresNumber(params) {
  return axios({
    url: '/api/income_expenditures/number/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'get',
    params,
    paramsSerializer,
  })
}

export function incomeExpendituresCreate(form) {
  return axios({
    url: '/api/income_expenditures/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'post',
    data: form,
  })
}

export function incomeExpendituresUpdate(form) {
  return axios({
    url: `/api/income_expenditures/${form.id}/`,
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'put',
    data: form,
  })
}

export function incomeExpendituresDestroy(form) {
  return axios({
    url: `/api/income_expenditures/${form.id}/`,
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'delete',
  })
}

// income_expenditure_projects
export function incomeExpenditureProjectsList(params) {
  return axios({
    url: '/api/income_expenditure_projects/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'get',
    params,
    paramsSerializer,
  })
}

export function incomeExpenditureProjectsCreate(form) {
  return axios({
    url: '/api/income_expenditure_projects/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'post',
    data: form,
  })
}

export function incomeExpenditureProjectsUpdate(form) {
  return axios({
    url: `/api/income_expenditure_projects/${form.id}/`,
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'put',
    data: form,
  })
}

export function incomeExpenditureProjectsReset(form) {
  return axios({
    url: `/api/income_expenditure_projects/${form.id}/`,
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'patch',
    data: form,
  })
}

export function incomeExpenditureProjectsDestroy(form) {
  return axios({
    url: `/api/income_expenditure_projects/${form.id}/`,
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    method: 'delete',
  })
}

