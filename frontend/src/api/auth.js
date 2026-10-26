import request from './request'

/**
 * 用户登录
 * @param {Object} data - { username, password }
 */
export const login = (data) => request.post('/login/', data)

/**
 * 获取当前用户信息
 */
export const getUserInfo = () => request.get('/user/info/')
