<template>
  <div class="login-container">
    <el-card class="login-card" shadow="always">
      <template #header>
        <div class="card-header">
          <el-icon size="32" color="#409eff"><School /></el-icon>
          <h2>高校科研项目申报与管理系统</h2>
          <p class="subtitle">请登录您的账号</p>
        </div>
      </template>

      <el-form
        :model="loginForm"
        :rules="rules"
        ref="loginRef"
        label-position="top"
        size="large"
      >
        <el-form-item label="用户名" prop="username">
          <el-input
            v-model="loginForm.username"
            placeholder="请输入用户名"
            clearable
            :prefix-icon="User"
          />
        </el-form-item>

        <el-form-item label="密码" prop="password">
          <el-input
            v-model="loginForm.password"
            type="password"
            show-password
            placeholder="请输入密码"
            :prefix-icon="Lock"
            @keyup.enter="handleLogin"
          />
        </el-form-item>

        <el-form-item style="margin-top: 8px;">
          <el-button
            type="primary"
            @click="handleLogin"
            :loading="loading"
            style="width: 100%"
            size="large"
          >
            登 录
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Lock, School } from '@element-plus/icons-vue'
import { login, getUserInfo } from '../api/auth'

const router = useRouter()
const loginRef = ref(null)
const loading = ref(false)

const loginForm = reactive({
  username: '',
  password: ''
})

const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur', min: 1 }]
}

// 根据角色跳转到对应首页
const redirectByRole = (role) => {
  if (role === 'admin') {
    router.push('/dashboard')
  } else if (role === 'expert') {
    router.push('/review')
  } else {
    // teacher
    router.push('/dashboard')
  }
}

const handleLogin = async () => {
  if (!loginRef.value) return
  await loginRef.value.validate(async (valid) => {
    if (!valid) return
    loading.value = true
    try {
      // 1. 获取 JWT Token
      const res = await login(loginForm)
      const { access } = res.data
      localStorage.setItem('token', access)

      // 2. 获取用户信息（角色等）
      let role = 'teacher'
      let username = loginForm.username
      try {
        const infoRes = await getUserInfo()
        role = infoRes.data.role || 'teacher'
        username = infoRes.data.username || loginForm.username
      } catch {
        // 若接口不存在，默认 teacher 角色
      }
      localStorage.setItem('role', role)
      localStorage.setItem('username', username)

      ElMessage.success('登录成功，欢迎回来！')
      redirectByRole(role)
    } catch (error) {
      // 错误已由拦截器处理，此处作兜底
      if (error.response?.status === 401 || error.response?.status === 400) {
        ElMessage.error('用户名或密码错误')
      }
    } finally {
      loading.value = false
    }
  })
}
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.login-card {
  width: 420px;
  border-radius: 12px;
}

.card-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 8px 0;
  gap: 6px;
}

.card-header h2 {
  margin: 0;
  font-size: 18px;
  color: #303133;
  text-align: center;
}

.subtitle {
  margin: 0;
  color: #909399;
  font-size: 13px;
}
</style>
