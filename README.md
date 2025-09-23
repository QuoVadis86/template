# FastAPI Template

一个简洁、开箱即用的 FastAPI 项目模板，专为内部 API 和微服务设计。

## 🚀 特性

- ⚡ **高性能**: 基于 FastAPI 和 Uvicorn
- 🐳 **Docker 支持**: 完整的 Docker 和 Docker Compose 配置
- 📦 **模块化结构**: 清晰的路由和服务分离
- 🔧 **生产就绪**: 包含 Gunicorn 配置
- 📚 **自动文档**: 自动生成 Swagger UI 和 ReDoc 文档
- 🎯 **简约设计**: 专注于 API 开发，无多余依赖
- 🔄 **统一响应**: 所有接口采用统一的响应格式

## 📁 项目结构

```
template/
├── main.py                 # 应用入口点
├── requirements.txt        # Python 依赖
├── Dockerfile              # Docker 构建配置
├── docker-compose.yml      # Docker Compose 配置
├── .dockerignore           # Docker 忽略文件
├── .gitignore              # Git 忽略文件
├── models/                 # 数据模型定义
│   └── __init__.py         # 通用响应模型
├── utils/                  # 工具函数
│   └── __init__.py         # 响应处理工具
├── routers/                # 路由模块
│   ├── tasks.py            # 任务相关接口
│   ├── nodes.py            # 节点状态接口
│   └── system.py           # 系统管理接口
└── services/               # 业务逻辑服务（可选）
```

## 🛠️ 快速开始

### 方式一：使用 Docker Compose（推荐用于开发）

```bash
# 克隆模板
git clone <your-repo-url> my-project
cd my-project

# 启动开发环境（带热重载）
docker-compose up

# 访问 API 文档
# Swagger UI: http://localhost:8000/docs
# ReDoc: http://localhost:8000/redoc
```

### 方式二：使用 Docker

```bash
# 构建镜像
docker build -t my-fastapi-app .

# 运行容器
docker run -d -p 8000:8000 --name my-api my-fastapi-app
```

### 方式三：本地开发

```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 安装依赖
pip install -r requirements.txt

# 启动开发服务器
uvicorn main:app --reload
```

## 📋 可用接口

模板包含以下示例接口：

- `GET /` - 根端点
- `POST /api/v1/tasks/` - 创建任务
- `GET /api/v1/tasks/{task_id}` - 获取任务状态
- `GET /api/v1/nodes/` - 获取节点状态
- `GET /api/v1/system/health` - 健康检查

## 🔄 统一响应格式

所有接口都使用统一的响应格式，包含以下字段：

```json
{
  "code": 200,
  "message": "success",
  "data": {},
  "error": null
}
```

字段说明：
- `code`: 响应码（200 表示成功，其他表示错误）
- `message`: 响应消息
- `data`: 返回的数据
- `error`: 错误详情（成功时为 null）

## 🔧 配置

### 环境变量

- `PORT`: 服务端口（默认: 8000）

### 添加新路由

1. 在 `routers/` 目录创建新文件
2. 使用 `APIRouter()` 创建路由实例
3. 使用 `success_response()` 和 `error_response()` 处理响应
4. 在 `main.py` 中导入并包含路由

示例：

```python
# routers/new_module.py
from fastapi import APIRouter
from models import ResponseModel
from utils import success_response, error_response

router = APIRouter()

@router.get("/endpoint", response_model=ResponseModel)
async def new_endpoint():
    return success_response(
        data={"message": "Hello World"},
        message="请求成功"
    )
```

```python
# main.py
from routers import new_module

app.include_router(new_module.router, prefix="/api/v1/new", tags=["new"])
```

## 🐳 生产部署

### 使用 Docker

```bash
docker build -t your-registry/your-app:latest .
docker push your-registry/your-app:latest
```

### 使用 Docker Compose

```bash
docker-compose -f docker-compose.prod.yml up -d
```

## 📝 许可证

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

⭐ 如果这个模板对你有帮助，请给它一个 Star！