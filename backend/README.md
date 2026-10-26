# Django 后端

此目录包含 Django 项目 `research_system`、用户与科研项目应用、已有数据库迁移和示例数据脚本。

从本目录运行管理命令：

```shell
python -m pip install -r requirements.txt
python manage.py check
python manage.py migrate
python manage.py runserver 8000
```

需要事先创建 MySQL 数据库，并通过操作系统环境变量设置数据库密码等配置。请先阅读[根目录启动说明](../README.md)。

`.env.example` 只是变量参考，代码不会自动加载 `.env` 文件。不要把真实密码提交到 GitHub。
