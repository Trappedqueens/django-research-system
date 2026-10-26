<template>
  <el-container style="min-height: 100vh;">
    <!-- 顶部导航栏 -->
    <el-header class="app-header">
      <div class="header-left">
        <el-icon size="22" color="#fff"><DataBoard /></el-icon>
        <span class="header-title">高校科研项目管理系统</span>
      </div>
      <div class="header-right">
        <el-tag :type="roleTagType" size="small" style="margin-right: 12px;">
          {{ roleLabel }}
        </el-tag>
        <span style="color: #ecf0f1; margin-right: 16px;">{{ username }}</span>
        <el-button
          v-if="role === 'teacher'"
          type="success"
          size="small"
          :icon="Plus"
          @click="$router.push('/apply')"
          style="margin-right: 12px;"
        >
          申报项目
        </el-button>
        <el-button
          v-if="role === 'expert' || role === 'admin'"
          type="warning"
          size="small"
          @click="$router.push('/review')"
          style="margin-right: 12px;"
        >
          审核中心
        </el-button>
        <el-button type="danger" size="small" :icon="SwitchButton" @click="handleLogout">
          退出
        </el-button>
      </div>
    </el-header>

    <!-- 主内容区 -->
    <el-main>
      <el-card shadow="never">
        <!-- 搜索与筛选工具栏 -->
        <el-row :gutter="16" style="margin-bottom: 20px;" align="middle">
          <el-col :span="8">
            <el-input
              v-model="searchText"
              placeholder="搜索项目名称..."
              clearable
              :prefix-icon="Search"
              @input="handleSearch"
              @clear="handleSearch"
            />
          </el-col>
          <el-col :span="5">
            <el-select
              v-model="statusFilter"
              placeholder="按状态筛选"
              clearable
              @change="fetchProjects"
              style="width: 100%"
            >
              <el-option label="全部" value="" />
              <el-option label="待审核" value="pending" />
              <el-option label="已通过" value="approved" />
              <el-option label="已拒绝" value="rejected" />
            </el-select>
          </el-col>
          <el-col :span="3">
            <el-button :icon="Refresh" @click="fetchProjects" circle title="刷新" />
          </el-col>
          <el-col :span="8" style="text-align: right;">
            <span style="color: #909399; font-size: 13px;">共 {{ total }} 条记录</span>
          </el-col>
        </el-row>

        <!-- 项目列表表格 -->
        <el-table
          :data="projects"
          v-loading="loading"
          border
          stripe
          style="width: 100%"
        >
          <el-table-column type="index" label="#" width="55" align="center" />
          <el-table-column prop="title" label="项目名称" min-width="180" show-overflow-tooltip />
          <el-table-column prop="category" label="项目类型" width="120" />
          <el-table-column prop="applicant_name" label="申报人" width="100" align="center" />
          <el-table-column prop="college" label="所属学院" width="140" show-overflow-tooltip />
          <el-table-column prop="budget" label="经费（元）" width="120" align="right">
            <template #default="scope">
              {{ Number(scope.row.budget).toLocaleString() }}
            </template>
          </el-table-column>
          <el-table-column prop="status" label="状态" width="100" align="center">
            <template #default="scope">
              <el-tag :type="statusTagType(scope.row.status)" size="small">
                {{ statusLabel(scope.row.status) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="created_at" label="申报时间" width="160" align="center">
            <template #default="scope">
              {{ formatDate(scope.row.created_at) }}
            </template>
          </el-table-column>
          <el-table-column label="操作" width="150" align="center" fixed="right">
            <template #default="scope">
              <el-button
                v-if="canAudit(scope.row)"
                type="primary"
                size="small"
                :icon="Edit"
                @click="handleAudit(scope.row)"
              >
                审核
              </el-button>
              <el-tag v-else-if="scope.row.status !== 'pending'" type="info" size="small">
                已处理
              </el-tag>
              <span v-else style="color: #c0c4cc; font-size: 12px;">—</span>
            </template>
          </el-table-column>
        </el-table>

        <!-- 分页 -->
        <div style="margin-top: 20px; display: flex; justify-content: flex-end;">
          <el-pagination
            v-model:current-page="currentPage"
            v-model:page-size="pageSize"
            :page-sizes="[10, 20, 50]"
            layout="total, sizes, prev, pager, next, jumper"
            :total="total"
            background
            @size-change="fetchProjects"
            @current-change="fetchProjects"
          />
        </div>
      </el-card>
    </el-main>
  </el-container>

  <!-- 审核对话框 -->
  <el-dialog
    v-model="dialogVisible"
    title="项目审核"
    width="500px"
    :close-on-click-modal="false"
  >
    <div class="audit-project-info" v-if="currentProject">
      <p><strong>项目名称：</strong>{{ currentProject.title }}</p>
      <p><strong>申报人：</strong>{{ currentProject.applicant_name }}</p>
      <p><strong>所属学院：</strong>{{ currentProject.college }}</p>
    </div>
    <el-divider />
    <el-form :model="auditForm" :rules="auditRules" ref="auditRef" label-width="80px">
      <el-form-item label="审核意见" prop="comment">
        <el-input
          v-model="auditForm.comment"
          type="textarea"
          :rows="4"
          placeholder="请填写审核意见..."
        />
      </el-form-item>
      <el-form-item label="审核结果" prop="result">
        <el-radio-group v-model="auditForm.result">
          <el-radio value="approved">
            <el-tag type="success" size="small">通过</el-tag>
          </el-radio>
          <el-radio value="rejected">
            <el-tag type="danger" size="small">拒绝</el-tag>
          </el-radio>
        </el-radio-group>
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="dialogVisible = false">取消</el-button>
      <el-button type="primary" :loading="submitLoading" @click="submitAudit">提交审核</el-button>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  DataBoard, Plus, SwitchButton, Search,
  Refresh, Edit
} from '@element-plus/icons-vue'
import { getProjects, auditProject } from '../api/project'

const router = useRouter()
const role = localStorage.getItem('role') || 'teacher'
const username = localStorage.getItem('username') || '用户'

// 状态
const projects = ref([])
const loading = ref(false)
const submitLoading = ref(false)
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(10)
const searchText = ref('')
const statusFilter = ref('')
const dialogVisible = ref(false)
const currentProject = ref(null)
const auditRef = ref(null)
const auditForm = ref({ comment: '', result: 'approved' })

const auditRules = {
  comment: [{ required: true, message: '请填写审核意见', trigger: 'blur' }],
  result: [{ required: true, message: '请选择审核结果', trigger: 'change' }]
}

// 角色标签
const roleLabel = computed(() => {
  const map = { admin: '管理员', teacher: '教师', expert: '专家' }
  return map[role] || role
})
const roleTagType = computed(() => {
  const map = { admin: 'danger', teacher: 'success', expert: 'warning' }
  return map[role] || 'info'
})

// 状态映射
const statusLabel = (status) => {
  const map = { pending: '待审核', approved: '已通过', rejected: '已拒绝' }
  return map[status] || status
}
const statusTagType = (status) => {
  const map = { pending: 'warning', approved: 'success', rejected: 'danger' }
  return map[status] || 'info'
}

// 是否可以审核
const canAudit = (row) => {
  return (role === 'expert' || role === 'admin') && row.status === 'pending'
}

// 格式化日期
const formatDate = (dateStr) => {
  if (!dateStr) return '—'
  return new Date(dateStr).toLocaleString('zh-CN', {
    year: 'numeric', month: '2-digit', day: '2-digit',
    hour: '2-digit', minute: '2-digit'
  })
}

// 搜索防抖
let searchTimer = null
const handleSearch = () => {
  clearTimeout(searchTimer)
  searchTimer = setTimeout(() => {
    currentPage.value = 1
    fetchProjects()
  }, 400)
}

// 拉取项目列表
const fetchProjects = async () => {
  loading.value = true
  try {
    const res = await getProjects({
      page: currentPage.value,
      page_size: pageSize.value,
      status: statusFilter.value || undefined,
      search: searchText.value || undefined
    })
    // 支持 DRF 分页格式 {count, results} 和普通数组
    if (res.data?.results !== undefined) {
      projects.value = res.data.results
      total.value = res.data.count
    } else {
      projects.value = res.data
      total.value = res.data.length
    }
  } catch {
    // 错误由拦截器统一处理
  } finally {
    loading.value = false
  }
}

// 打开审核弹框
const handleAudit = (row) => {
  currentProject.value = row
  auditForm.value = { comment: '', result: 'approved' }
  dialogVisible.value = true
}

// 提交审核
const submitAudit = async () => {
  if (!auditRef.value) return
  await auditRef.value.validate(async (valid) => {
    if (!valid) return
    submitLoading.value = true
    try {
      await auditProject(currentProject.value.id, auditForm.value)
      ElMessage.success('审核意见已提交')
      dialogVisible.value = false
      fetchProjects()
    } finally {
      submitLoading.value = false
    }
  })
}

// 退出登录
const handleLogout = async () => {
  await ElMessageBox.confirm('确定要退出登录吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).catch(() => {})
  localStorage.clear()
  ElMessage.success('已退出登录')
  router.push('/login')
}

onMounted(fetchProjects)
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
  letter-spacing: 1px;
}

.header-right {
  display: flex;
  align-items: center;
}

.audit-project-info {
  background: #f5f7fa;
  border-radius: 6px;
  padding: 12px 16px;
}

.audit-project-info p {
  margin: 6px 0;
  font-size: 14px;
  color: #606266;
}
</style>
