# 高校科研项目申报与管理系统

基于 **Django REST Framework + Vue 3 + Element Plus** 的前后端分离项目。此仓库直接整合 GitHub 上的 `Django-backend` 和 `Django-vue3`，在同一项目目录下分别维护后端与前端源码。

## 项目结构

```text
django-research-system/
├─ backend/
│  ├─ manage.py
│  ├─ requirements.txt
│  ├─ .env.example
│  ├─ research_system/        Django 配置、路由与 WSGI
│  ├─ apps/
│  │  ├─ users/              用户、JWT 登录及角色
│  │  └─ projects/           科研项目与审核记录
│  └─ init_data.py           示例数据初始化
├─ frontend/
│  ├─ package.json
│  ├─ package-lock.json
│  ├─ vite.config.js
│  └─ src/                   Vue 页面、路由和 API
├─ docs/                     需求、数据库设计和迁移来源
├─ deploy/                   Nginx 配置示例
└─ tools/                    原仓库的辅助绘图脚本
```

这是普通的单仓库结构，`backend/` 与 `frontend/` 均为实际文件目录，不是 Git 子模块。前端保留 Vue 源码，可以重新构建。

## 现有功能

| 模块 | 内容 |
| --- | --- |
| 登录与用户 | 注册、JWT 登录、刷新令牌、当前用户信息；管理员、教师、专家角色 |
| 科研申报 | 项目名称、类型、学院、预算、描述；项目列表、分页、搜索和状态筛选 |
| 项目审核 | 管理员或专家审核、意见与结果记录，待审核/已通过/已拒绝状态 |
| 前端页面 | 登录、项目看板、申报、审核及未找到页面；路由登录和角色守卫 |
| 管理后台 | Django Admin 用户、科研项目和审核记录管理 |
| 示例数据 | 本地演示用户及科研项目初始化脚本 |

本次主要整理代码目录与运行配置，没有重新实现这些业务功能。来源与改动范围见 [docs/SOURCES.md](docs/SOURCES.md)。

## 环境

- Python 3.12、MySQL，以及系统所需的 MySQL 客户端开发依赖。
- Node.js 与 npm：Vite 锁定版本声明支持 Node 18、20 或 22+，请使用与该工具链兼容的版本。
- 前后端依赖分别见 `backend/requirements.txt` 和 `frontend/package-lock.json`。

## 获取代码

```shell
git clone https://github.com/Trappedqueens/django-research-system.git
cd django-research-system
```

## 后端启动

以下命令都在 `backend/` 目录执行。

### 1. 创建 Python 环境并安装依赖

Windows PowerShell：

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Linux / macOS：

```bash
cd backend
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

后续命令中的 `python` 指已激活环境中的 Python；Windows 若未激活，可使用 `.\.venv\Scripts\python.exe` 替代。

### 2. 准备 MySQL 与环境变量

先创建数据库：

```sql
CREATE DATABASE research_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;
```

使用有权限访问该数据库的账号。Windows PowerShell 示例：

```powershell
$env:DB_NAME = 'research_db'
$env:DB_USER = 'your_mysql_user'
$env:DB_PASSWORD = 'your_mysql_password'
$env:DB_HOST = '127.0.0.1'
$env:DB_PORT = '3306'
```

Linux / macOS 示例：

```bash
export DB_NAME=research_db
export DB_USER=your_mysql_user
export DB_PASSWORD=your_mysql_password
export DB_HOST=127.0.0.1
export DB_PORT=3306
```

`backend/.env.example` 仅作为变量参考，Django **不会自动加载** `.env` 文件。请在运行服务的终端或服务管理配置中设置变量；不要把真实密码写入代码或提交到仓库。

### 3. 检查与迁移

```shell
python manage.py check
python manage.py migrate
```

仓库已保留原有迁移文件，首次使用不需要重新运行 `makemigrations`。

### 4. 创建账号并运行

自行创建管理员：

```shell
python manage.py createsuperuser
python manage.py runserver 8000
```

原前端按扩展字段 `role` 区分管理员、教师和专家；Django 超级用户的 `is_superuser` 不等同于业务角色。需要完整的演示账号与项目时，先自行设置 `DEMO_ADMIN_PASSWORD`、`DEMO_TEACHER_PASSWORD`、`DEMO_EXPERT_PASSWORD` 三个环境变量，再在空的开发数据库中运行：

```shell
python init_data.py
```

示例账号：

| 角色 | 用户名 | 示例密码 |
| --- | --- | --- |
| 管理员 | `admin` | 从 `DEMO_ADMIN_PASSWORD` 读取 |
| 教师 | `teacher01`、`teacher02` | 从 `DEMO_TEACHER_PASSWORD` 读取 |
| 专家 | `expert01` | 从 `DEMO_EXPERT_PASSWORD` 读取 |

演示密码由运行者自行设置，仓库不再提供固定密码；未设置三个变量时，初始化脚本会停止。脚本会写入数据库，只在隔离的开发数据库中使用。

后端地址：[http://localhost:8000/](http://localhost:8000/)；该根路径未必提供页面，API 位于 `/api/`，管理后台位于 [http://localhost:8000/admin/](http://localhost:8000/admin/)。

## 前端启动

另开一个终端，在仓库根目录运行：

```shell
cd frontend
npm ci
npm run dev
```

打开 [http://localhost:5173/](http://localhost:5173/)。

前端请求使用相对路径 `/api`。开发时 Vite 会将它代理到 `http://localhost:8000`，因此不需要把后端绝对地址写进页面。改后端端口时，同步调整 `frontend/vite.config.js`。

构建前端：

```shell
npm run build
```

输出目录为 `frontend/dist/`。`npm run preview` 仅用于预览构建结果，没有配置后端代理；完整联调请使用开发服务器或下方的 Nginx 配置。

## 部署目录调整

迁移后，服务器应分别使用：

- 后端工作目录：`/srv/django-research-system/backend`。
- 前端静态目录：`/srv/django-research-system/frontend/dist`。
- Django 静态收集目录：`/srv/django-research-system/backend/staticfiles`。

可参考 [deploy/nginx.conf.example](deploy/nginx.conf.example)。先按实际路径和域名修改配置，并准备自己的 HTTPS 与服务管理方案。

后端生产配置使用环境变量：

| 变量 | 默认值 / 说明 |
| --- | --- |
| `DJANGO_DEBUG` | `true`；生产环境设置为 `false` |
| `DJANGO_SECRET_KEY` | 开发占位值；生产必须设置独立的私密随机值，否则拒绝启动 |
| `DJANGO_ALLOWED_HOSTS` | `localhost,127.0.0.1`；生产填写实际域名，多个值用逗号分隔 |
| `DB_NAME` | `research_db` |
| `DB_USER` | `root`；建议使用独立数据库账号 |
| `DB_PASSWORD` | 默认为空，按实际数据库设置 |
| `DB_HOST` / `DB_PORT` | `127.0.0.1` / `3306` |

在 `backend/` 中收集静态资源：

```shell
python manage.py collectstatic --noinput
```

如使用 Gunicorn，需自行安装该部署依赖，并从 `backend/` 运行：

```shell
gunicorn research_system.wsgi:application --bind 127.0.0.1:8000
```

Nginx 示例对 `/api/` 的 `proxy_pass` 没有末尾斜杠，用于保留后端需要的 `/api/` 路径。本次没有连接服务器、修改原线上目录或重启任何线上服务。

## 迁移与验证说明

- 前端完整目录搬到 `frontend/`，其中相对导入关系与锁定文件保持配套。
- 后端应用、项目包和迁移整体位于 `backend/`；`manage.py` 与 `research_system` 的相对关系不变。
- 数据库连接改为环境变量；没有携带数据库文件或数据库内容。
- 忽略 IDE 配置、日志、虚拟环境、依赖目录、构建目录及真实环境配置。
- 原来的两个 GitHub 仓库保留，迁移使用的源提交记录在 [docs/SOURCES.md](docs/SOURCES.md)。
- 本次以 GitHub 快照为来源进行目录迁移与配置整理，进行了结构、导入路径和配置一致性检查，**没有本地构建、运行测试或数据库迁移**。首次部署请执行上面的检查与构建命令。

`tools/generate_vsdx.py` 是原仓库的辅助脚本，引用的 `zwm.vsdx` 模板未包含在源仓库中；它不参与前后端启动。
