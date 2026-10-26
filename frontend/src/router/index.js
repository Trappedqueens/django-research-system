import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/', redirect: '/login' },
  {
    path: '/login',
    component: () => import('../views/Login.vue'),
    meta: { public: true }
  },
  {
    path: '/dashboard',
    component: () => import('../views/Dashboard.vue'),
    meta: { roles: ['admin', 'teacher', 'expert'] }
  },
  {
    path: '/apply',
    component: () => import('../views/Apply.vue'),
    meta: { roles: ['teacher'] }
  },
  {
    path: '/review',
    component: () => import('../views/Review.vue'),
    meta: { roles: ['expert', 'admin'] }
  },
  {
    path: '/:pathMatch(.*)*',
    component: () => import('../views/NotFound.vue'),
    meta: { public: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫：未登录拦截 + 角色权限控制
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  const role = localStorage.getItem('role')

  // 公开路由直接放行
  if (to.meta.public) {
    if (token && to.path === '/login') {
      return next(role === 'expert' ? '/review' : '/dashboard')
    }
    return next()
  }

  // 未登录
  if (!token) {
    return next('/login')
  }

  // 角色权限校验
  if (to.meta.roles && !to.meta.roles.includes(role)) {
    return next(role === 'expert' ? '/review' : '/dashboard')
  }

  next()
})

export default router
