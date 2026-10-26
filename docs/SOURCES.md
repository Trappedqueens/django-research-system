# 迁移来源与范围

本仓库以 GitHub 上的以下快照为来源，未使用本地同名 Django 项目作为迁移来源：

| 内容 | 源仓库 | 源提交 |
| --- | --- | --- |
| Vue 前端与原始设计文档 | [Trappedqueens/Django-vue3](https://github.com/Trappedqueens/Django-vue3) | `f3abb12e40852211e3b1dd4c8f8639b47884f90f` |
| Django 后端 | [Trappedqueens/Django-backend](https://github.com/Trappedqueens/Django-backend) | `f2afbd2ef3bf64edf835e7f7198df9bc8d6c6ef0` |

迁移映射：

- `Django-vue3/Django-Management web/*` → `frontend/*`。
- 后端应用、项目配置、依赖、迁移和初始化脚本 → `backend/*`。
- 原前端仓库的需求与数据库设计文档 → `docs/`。
- 原 `generate_vsdx.py` → `tools/generate_vsdx.py`。

原来的两个仓库保留。本次是代码快照整理，不将两个仓库的所有历史提交合并到新仓库历史中；旧历史仍可在源仓库查看。

额外调整仅用于统一项目运行和配置：

- 更新根目录及子目录启动说明。
- 数据库连接参数、Django 密钥、调试开关与允许主机改为读取环境变量。
- 将示例数据脚本的固定演示密码改为从 `DEMO_*_PASSWORD` 环境变量读取；未设置时停止初始化。
- 为 `collectstatic` 指定输出目录。
- 增加忽略规则、环境变量参考和部署示例。
- 不携带 IDE 配置、日志、虚拟环境、数据库文件或前端依赖目录。

未在本地安装依赖、启动服务或访问真实数据库。检查范围为 GitHub 文件快照、目录结构、依赖锁定文件、相对导入和接口路径；不宣称已完成构建或运行测试。
