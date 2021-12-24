import request from '@/utils/request';

// Permission
export function permissionList(params) {
  return request({ url: `/permission_groups/`, method: 'get', params })
}

// 系统配置
export function configInfo(params) {
  return request({ url: `/system/configs/`, method: 'get', params })
}

// 系统配置-更新
export function configUpdate(data) {
  return request({ url: `/system/set_configs/`, method: 'post', data })
}
