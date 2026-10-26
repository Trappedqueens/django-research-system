# Vue 前端

此目录保留完整的 Vue 3 源码、Vite 配置及 npm 锁定文件。

```shell
npm ci
npm run dev
```

开发地址为 `http://localhost:5173`，`/api` 自动代理到 `http://localhost:8000`。请先启动 `../backend` 中的 Django 服务。

```shell
npm run build
npm run preview
```

生产构建输出在 `frontend/dist/`，不会提交到仓库。完整安装与部署说明见[根目录 README](../README.md)。
