import request from './request'

/**
 * 获取项目列表（支持分页与过滤）
 * @param {Object} params - { page, page_size, status, search }
 */
export const getProjects = (params) => request.get('/projects/', { params })

/**
 * 获取项目详情
 * @param {number} id
 */
export const getProjectDetail = (id) => request.get(`/projects/${id}/`)

/**
 * 提交项目申报
 * @param {Object} data - 项目表单数据
 */
export const createProject = (data) => request.post('/projects/', data)

/**
 * 审核项目（专家/管理员）
 * @param {number} id
 * @param {Object} data - { comment, result }
 */
export const auditProject = (id, data) => request.post(`/projects/${id}/audit/`, data)
