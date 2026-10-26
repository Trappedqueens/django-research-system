<template>
  <el-container style="min-height: 100vh;">
    <!-- 顶部导航栏 -->
    <el-header class="app-header">
      <div class="header-left">
        <el-icon size="22" color="#fff"><EditPen /></el-icon>
        <span class="header-title">项目申报</span>
      </div>
      <div class="header-right">
        <el-button
          size="small"
          :icon="ArrowLeft"
          @click="$router.push('/dashboard')"
          style="margin-right: 12px;"
        >
          返回列表
        </el-button>
        <span style="color: #ecf0f1;">{{ username }}</span>
      </div>
    </el-header>

    <!-- 主内容区 -->
    <el-main>
      <el-card shadow="never" style="max-width: 700px; margin: 0 auto;">
        <template #header>
          <div style="display: flex; align-items: center; gap: 8px;">
            <el-icon color="#409eff"><EditPen /></el-icon>
            <span style="font-size: 16px; font-weight: 600;">新建项目申报</span>
          </div>
        </template>

        <el-form
          :model="form"
          :rules="rules"
          ref="formRef"
          label-width="110px"
          size="large"
        >
          <el-form-item label="项目名称" prop="title">
            <el-input
              v-model="form.title"
              placeholder="请输入项目名称（5~100字）"
              clearable
              maxlength="100"
              show-word-limit
            />
          </el-form-item>

          <el-form-item label="项目类型" prop="category">
            <el-select v-model="form.category" placeholder="请选择项目类型" style="width: 100%">
              <el-option label="国家级自然科学基金" value="国家级自然科学基金" />
              <el-option label="省级科研项目" value="省级科研项目" />
              <el-option label="横向合作项目" value="横向合作项目" />
              <el-option label="校级重点项目" value="校级重点项目" />
              <el-option label="青年基金项目" value="青年基金项目" />
              <el-option label="其他" value="其他" />
            </el-select>
          </el-form-item>

          <el-form-item label="所属学院" prop="college">
            <el-input
              v-model="form.college"
              placeholder="请输入所属学院"
              clearable
            />
          </el-form-item>

          <el-form-item label="申请经费（元）" prop="budget">
            <el-input-number
              v-model="form.budget"
              :min="0"
              :max="99999999"
              :precision="2"
              :step="10000"
              controls-position="right"
              style="width: 100%"
            />
          </el-form-item>

          <el-form-item label="项目描述" prop="description">
            <el-input
              v-model="form.description"
              type="textarea"
              :rows="6"
              placeholder="请详细描述项目背景、目标、研究内容及预期成果（不少于20字）"
              maxlength="2000"
              show-word-limit
            />
          </el-form-item>

          <el-form-item>
            <el-button
              type="primary"
              :loading="loading"
              :icon="Check"
              size="large"
              @click="onSubmit"
            >
              立即申报
            </el-button>
            <el-button size="large" :icon="Close" @click="$router.push('/dashboard')">
              取消
            </el-button>
          </el-form-item>
        </el-form>
      </el-card>
    </el-main>
  </el-container>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { EditPen, ArrowLeft, Check, Close } from '@element-plus/icons-vue'
import { createProject } from '../api/project'

const router = useRouter()
const username = localStorage.getItem('username') || '用户'
const formRef = ref(null)
const loading = ref(false)

const form = reactive({
  title: '',
  category: '',
  college: '',
  budget: 0,
  description: ''
})

const rules = {
  title: [
    { required: true, message: '请输入项目名称', trigger: 'blur' },
    { min: 5, max: 100, message: '项目名称长度在 5 到 100 个字符', trigger: 'blur' }
  ],
  category: [{ required: true, message: '请选择项目类型', trigger: 'change' }],
  college: [{ required: true, message: '请输入所属学院', trigger: 'blur' }],
  budget: [{ required: true, message: '请填写申请经费', trigger: 'blur' }],
  description: [
    { required: true, message: '请填写项目描述', trigger: 'blur' },
    { min: 20, message: '项目描述不少于20个字', trigger: 'blur' }
  ]
}

const onSubmit = async () => {
  if (!formRef.value) return
  await formRef.value.validate(async (valid) => {
    if (!valid) return
    loading.value = true
    try {
      await createProject(form)
      ElMessage.success('项目申报成功，等待审核！')
      router.push('/dashboard')
    } finally {
      loading.value = false
    }
  })
}
</script>

<style scoped>
.app-header {
  background: linear-gradient(90deg, #409eff, #2c7be5);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.header-left {
  display: flex;
  align-items: center;
  gap: 10px;
}

.header-title {
  color: #fff;
  font-size: 17px;
  font-weight: 600;
}

.header-right {
  display: flex;
  align-items: center;
}
</style>
