# Template

一个简洁、开箱即用的 FastAPI 项目模板，专为内部 API 和微服务设计。

## 🚀 特性

- ⚡ **高性能**: 基于 FastAPI 和 Uvicorn
- 🐳 **Docker 支持**: 完整的 Docker 和 Docker Compose 配置
- 📦 **模块化结构**: 清晰的路由和服务分离
- 🔧 **生产就绪**: 包含 Gunicorn 配置
- 📚 **自动文档**: 自动生成 Swagger UI 和 ReDoc 文档
- 🎯 **简约设计**: 专注于 API 开发，无多余依赖

## 📁 项目结构
template/
├── main.py # 应用入口点
├── requirements.txt # Python 依赖
├── Dockerfile # Docker 构建配置
├── docker-compose.yml # Docker Compose 配置
├── .dockerignore # Docker 忽略文件
├── .gitignore # Git 忽略文件
├── routers/ # 路由模块
│ ├── tasks.py # 任务相关接口
│ ├── nodes.py # 节点状态接口
│ └── system.py # 系统管理接口
└── services/ # 业务逻辑服务（可选）

## 🛠️ 快速开始

### 方式一：使用 Docker Compose（推荐用于开发）

```bash
# 克隆模板
git clone <your-repo-url> my-project
cd my-project

# 启动开发环境（带热重载）
docker-compose up

# 访问 API 文档
# Swagger UI: http://localhost:8000/swagger 
# Doc: http://localhost:8000/docs 用于展示，不能调试