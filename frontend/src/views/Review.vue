<template>
  <el-container style="min-height: 100vh;">
    <!-- 顶部导航栏 -->
    <el-header class="app-header">
      <div class="header-left">
        <el-icon size="22" color="#fff"><Stamp /></el-icon>
        <span class="header-title">审核中心</span>
      </div>
      <div class="header-right">
        <el-tag :type="roleTagType" size="small" style="margin-right: 12px;">{{ roleLabel }}</el-tag>
        <span style="color: #ecf0f1; margin-right: 16px;">{{ username }}</span>
        <el-button size="small" :icon="House" @click="$router.push('/dashboard')" style="margin-right: 12px;">
          项目列表
        </el-button>
        <el-button type="danger" size="small" :icon="SwitchButton" @click="handleLogout">
          退出
        </el-button>
      </div>
    </el-header>

    <!-- 主内容区 -->
    <el-main>
      <el-card shadow="never">
        <!-- 页头统计 -->
        <el-row :gutter="16" style="margin-bottom: 24px;">
          <el-col :span="6">
            <el-statistic title="待审核" :value="pendingCount" value-style="color: #e6a23c;" />
          </el-col>
          <el-col :span="6">
            <el-statistic title="已通过" :value="approvedCount" value-style="color: #67c23a;" />
          </el-col>
          <el-col :span="6">
            <el-statistic title="已拒绝" :value="rejectedCount" value-style="color: #f56c6c;" />
          </el-col>
          <el-col :span="6">
            <el-statistic title="总计" :value="total" />
          </el-col>
        </el-row>

        <!-- 工具栏 -->
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
              placeholder="状态筛选"
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
        </el-row>

        <!-- 项目列表 -->
        <el-table
          :data="projects"
          v-loading="loading"
          border
          stripe
          style="width: 100%"
        >
          <el-table-column type="index" label="#" width="55" align="center" />
          <el-table-column prop="title" label="项目名称" min-width="180" show-overflow-tooltip />
          <el-table-column prop="category" label="项目类型" width="140" />
          <el-table-column prop="applicant_name" label="申报人" width="100" align="center" />
          <el-table-column prop="college" label="所属学院" width="140" show-overflow-tooltip />
          <el-table-column prop="budget" label="经费（元）" width="130" align="right">
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
          <el-table-column prop="created_at" label="申报时间" width="150" align="center">
            <template #default="scope">
              {{ formatDate(scope.row.created_at) }}
            </template>
          </el-table-column>
          <el-table-column label="操作" width="120" align="center" fixed="right">
            <template #default="scope">
              <el-button
                v-if="scope.row.status === 'pending'"
                type="primary"
                size="small"
                :icon="Stamp"
                @click="handleAudit(scope.row)"
              >
                审核
              </el-button>
              <el-button
                v-else
                size="small"
                :icon="View"
                @click="handleViewDetail(scope.row)"
              >
                详情
              </el-button>
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
    v-model="auditDialogVisible"
    title="提交审核意见"
    width="520px"
    :close-on-click-modal="false"
  >
    <div class="project-info-panel" v-if="currentProject">
      <el-descriptions :column="2" border size="small">
        <el-descriptions-item label="项目名称" :span="2">{{ currentProject.title }}</el-descriptions-item>
        <el-descriptions-item label="申报人">{{ currentProject.applicant_name }}</el-descriptions-item>
        <el-descriptions-item label="所属学院">{{ currentProject.college }}</el-descriptions-item>
        <el-descriptions-item label="项目类型">{{ currentProject.category }}</el-descriptions-item>
        <el-descriptions-item label="申请经费">{{ Number(currentProject.budget).toLocaleString() }} 元</el-descriptions-item>
        <el-descriptions-item label="项目描述" :span="2">{{ currentProject.description }}</el-descriptions-item>
      </el-descriptions>
    </div>
    <el-divider />
    <el-form :model="auditForm" :rules="auditRules" ref="auditRef" label-width="80px" style="margin-top: 8px;">
      <el-form-item label="审核结果" prop="result">
        <el-radio-group v-model="auditForm.result" size="large">
          <el-radio-button value="approved">
            <el-icon><Check /></el-icon> 通过
          </el-radio-button>
          <el-radio-button value="rejected">
            <el-icon><Close /></el-icon> 拒绝
          </el-radio-button>
        </el-radio-group>
      </el-form-item>
      <el-form-item label="审核意见" prop="comment">
        <el-input
          v-model="auditForm.comment"
          type="textarea"
          :rows="4"
          placeholder="请详细填写审核意见（必填）"
        />
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="auditDialogVisible = false">取消</el-button>
      <el-button type="primary" :loading="submitLoading" @click="submitAudit">提交</el-button>
    </template>
  </el-dialog>

  <!-- 详情查看对话框 -->
  <el-dialog
    v-model="detailDialogVisible"
    title="项目详情"
    width="560px"
  >
    <div v-if="currentProject">
      <el-descriptions :column="2" border>
        <el-descriptions-item label="项目名称" :span="2">{{ currentProject.title }}</el-descriptions-item>
        <el-descriptions-item label="申报人">{{ currentProject.applicant_name }}</el-descriptions-item>
        <el-descriptions-item label="所属学院">{{ currentProject.college }}</el-descriptions-item>
        <el-descriptions-item label="项目类型">{{ currentProject.category }}</el-descriptions-item>
        <el-descriptions-item label="申请经费">{{ Number(currentProject.budget).toLocaleString() }} 元</el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="statusTagType(currentProject.status)">{{ statusLabel(currentProject.status) }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="申报时间">{{ formatDate(currentProject.created_at) }}</el-descriptions-item>
        <el-descriptions-item label="项目描述" :span="2">{{ currentProject.description }}</el-descriptions-item>
      </el-descriptions>
    </div>
    <template #footer>
      <el-button @click="detailDialogVisible = false">关闭</el-button>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Stamp, House, SwitchButton, Search, Refresh,
  View, Check, Close
} from '@element-plus/icons-vue'
import { getProjects, auditProject } from '../api/project'

const router = useRouter()
const role = localStorage.getItem('role') || 'expert'
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
const auditDialogVisible = ref(false)
const detailDialogVisible = ref(false)
const currentProject = ref(null)
const auditRef = ref(null)
const auditForm = ref({ comment: '', result: 'approved' })

const auditRules = {
  result: [{ required: true, message: '请选择审核结果', trigger: 'change' }],
  comment: [{ required: true, message: '请填写审核意见', trigger: 'blur' }]
}

// 统计数据
const pendingCount = computed(() => projects.value.filter(p => p.status === 'pending').length)
const approvedCount = computed(() => projects.value.filter(p => p.status === 'approved').length)
const rejectedCount = computed(() => projects.value.filter(p => p.status === 'rejected').length)

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

// 拉取项目
const fetchProjects = async () => {
  loading.value = true
  try {
    const res = await getProjects({
      page: currentPage.value,
      page_size: pageSize.value,
      status: statusFilter.value || undefined,
      search: searchText.value || undefined
    })
    if (res.data?.results !== undefined) {
      projects.value = res.data.results
      total.value = res.data.count
    } else {
      projects.value = res.data
      total.value = res.data.length
    }
  } finally {
    loading.value = false
  }
}

// 打开审核弹框
const handleAudit = (row) => {
  currentProject.value = row
  auditForm.value = { comment: '', result: 'approved' }
  auditDialogVisible.value = true
}

// 查看详情
const handleViewDetail = (row) => {
  currentProject.value = row
  detailDialogVisible.value = true
}

// 提交审核
const submitAudit = async () => {
  if (!auditRef.value) return
  await auditRef.value.validate(async (valid) => {
    if (!valid) return
    submitLoading.value = true
    try {
      await auditProject(currentProject.value.id, auditForm.value)
      ElMessage.success('审核结果已提交')
      auditDialogVisible.value = false
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
  background: linear-gradient(90deg, #e6a23c, #d48806);
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

.project-info-panel {
  background: #f5f7fa;
  border-radius: 6px;
  padding: 4px;
}
</style>
