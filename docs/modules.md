# 项目模块详细说明

本文档详细介绍了项目中各个模块的功能和作用。

## 项目概述

这是一个基于 FastAPI 的后端 API 服务，用于调度系统。项目采用模块化设计，将不同功能的接口分离到不同的路由模块中，便于维护和扩展。

## 模块说明

### main.py - 应用入口点

这是整个应用的入口文件，负责：
- 初始化 FastAPI 应用实例
- 配置应用的基本信息（标题、描述、版本等）
- 注册所有路由模块
- 配置 API 文档路径

```python
from fastapi import FastAPI
from routers import tasks, nodes, system

app = FastAPI(
    title="Scheduler API",
    description="Internal API for scheduler backend",
    version="1.0.0",
    docs_url="/swagger",
    redoc_url="/docs",
)

# 注册所有路由
app.include_router(tasks.router, prefix="/api/v1/tasks", tags=["tassks"])
app.include_router(nodes.router, prefix="/api/v1/nodes", tags=["nodses"])
app.include_router(system.router, prefix="/api/v1/system", tags=["sysstem"])
```

### routers - 路由模块目录

该目录包含了所有的 API 路由定义，每个文件负责一类功能的接口。

#### routers/tasks.py - 任务管理模块

负责任务的创建、查询、停止等操作。

主要接口：
- `POST /` - 创建新任务
- `GET /{task_id}` - 获取任务状态
- `POST /{task_id}/stop` - 停止指定任务
- `GET /` - 列出所有任务

数据存储：目前使用内存字典模拟存储（实际项目中会替换为数据库或与调度器核心通信）

#### routers/nodes.py - 节点管理模块

负责管理系统节点状态，包括查看节点状态和节点管理操作。

主要接口：
- `GET /` - 获取所有节点状态
- `GET /{node_id}` - 获取特定节点状态
- `POST /{node_id}/drain` - 将节点设置为排水模式（不再接收新任务）

数据存储：目前使用内存字典模拟节点状态存储

#### routers/system.py - 系统管理模块

负责系统的健康检查、监控指标和系统级操作。

主要接口：
- `GET /health` - 健康检查端点
- `GET /metrics` - 获取系统指标
- `POST /restart` - 重启服务

### services - 业务逻辑服务目录

该目录用于存放业务逻辑实现代码。目前是空的，但按照项目结构设计，后续的业务逻辑应该放在这里，与路由层分离。

### 其他配置文件

#### requirements.txt - 项目依赖

定义了项目所需的所有 Python 包依赖：
- fastapi - 主要的 Web 框架
- uvicorn - ASGI 服务器
- python-multipart - 处理 multipart 请求
- python-dotenv - 环境变量加载
- gunicorn - 生产环境 WSGI 服务器

#### Dockerfile - Docker 镜像构建配置

用于构建项目的 Docker 镜像，包含了：
- 基于 python:3.11-slim 的基础镜像
- 系统依赖安装
- Python 依赖安装
- 应用代码复制
- 使用 gunicorn + uvicorn workers 的生产级运行配置

#### docker-compose.yml - 开发环境配置

用于本地开发环境的容器编排配置：
- 构建当前项目
- 映射端口 8000
- 设置环境变量
- 挂载本地代码卷以支持热重载
- 使用 uvicorn 开发服务器运行

#### README.md - 项目说明文档

项目的说明文档，包含了：
- 项目特性介绍
- 项目结构说明
- 快速开始指南（多种运行方式）
- 可用接口列表
- 配置说明
- 生产部署指南