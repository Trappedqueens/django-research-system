import axios from 'axios'
import { ElMessage } from 'element-plus'

const service = axios.create({
  baseURL: '/api',
  timeout: 10000
})

// 请求拦截器：自动附加 JWT Token
service.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token')
    if (token) config.headers.Authorization = `Bearer ${token}`
    return config
  },
  error => Promise.reject(error)
)

// 响应拦截器：统一错误处理
service.interceptors.response.use(
  response => response,
  error => {
    if (error.response) {
      const { status } = error.response
      if (status === 401) {
        ElMessage.error('登录已过期，请重新登录')
        localStorage.clear()
        window.location.href = '/login'
      } else if (status === 403) {
        ElMessage.error('权限不足，无法执行此操作')
      } else if (status === 500) {
        ElMessage.error('服务器内部错误，请稍后重试')
      } else {
        const msg = error.response.data?.detail || error.response.data?.message || '请求失败'
        ElMessage.error(msg)
      }
    } else {
      ElMessage.error('网络异常，请检查网络连接')
    }
    return Promise.reject(error)
  }
)

export default service
