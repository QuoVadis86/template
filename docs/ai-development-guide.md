# AI 开发指导文档

本文档旨在为后续的 AI 开发者提供项目上下文和开发指导，确保代码编写的规范性和一致性。

## 项目概述

这是一个基于 FastAPI 的调度系统后端 API 服务。项目采用模块化设计，遵循"路由-服务"分离的架构模式。

## 项目架构

```
template/
├── main.py                 # 应用入口点
├── requirements.txt        # Python 依赖
├── Dockerfile              # Docker 构建配置
├── docker-compose.yml      # Docker Compose 配置
├── .dockerignore           # Docker 忽略文件
├── .gitignore              # Git 忽略文件
├── routers/                # 路由模块
│   ├── tasks.py            # 任务相关接口
│   ├── nodes.py            # 节点状态接口
│   └── system.py           # 系统管理接口
└── services/               # 业务逻辑服务（可选）
```

## 开发规范

### 路由开发规范

1. 所有路由文件应放在 `routers/` 目录下
2. 每个路由文件应使用 `APIRouter()` 创建路由实例
3. 路由文件应专注于请求处理和响应格式化
4. 业务逻辑应放在 `services/` 目录下

示例路由文件结构：
```python
from fastapi import APIRouter

router = APIRouter()

@router.get("/endpoint")
async def endpoint_handler():
    return {"message": "Hello World"}
```

### 服务开发规范

1. 所有业务逻辑应封装在 `services/` 目录下的服务类或函数中
2. 服务应专注于业务逻辑实现，不直接处理 HTTP 请求/响应
3. 服务函数应具有明确的输入和输出

示例服务结构：
```python
class TaskService:
    def create_task(self, config: dict) -> dict:
        # 实现业务逻辑
        pass
    
    def get_task_status(self, task_id: str) -> dict:
        # 实现业务逻辑
        pass
```

## 开发流程

### 添加新功能的步骤

1. 分析功能需求，确定是否需要新的路由模块
2. 如果需要新路由：
   - 在 `routers/` 目录下创建新的路由文件
   - 使用 `APIRouter()` 创建路由实例
   - 实现相应的路由处理函数
   - 在 [main.py](file:///Users/meta001/Documents/GitHub/template/main.py) 中注册新路由

3. 实现业务逻辑：
   - 如果业务逻辑简单，可以直接在路由处理函数中实现
   - 如果业务逻辑复杂，应在 `services/` 目录下创建相应的服务类或函数

4. 确保添加适当的错误处理和数据验证

### 路由注册

在 [main.py](file:///Users/meta001/Documents/GitHub/template/main.py) 中注册路由的示例：

```python
# 导入路由模块
from routers import tasks, nodes, system, new_module

# 注册路由
app.include_router(tasks.router, prefix="/api/v1/tasks", tags=["tasks"])
app.include_router(nodes.router, prefix="/api/v1/nodes", tags=["nodes"])
app.include_router(system.router, prefix="/api/v1/system", tags=["system"])
app.include_router(new_module.router, prefix="/api/v1/new", tags=["new"])
```

## API 设计原则

### RESTful 设计

1. 使用合适的 HTTP 方法：
   - GET: 获取资源
   - POST: 创建资源或执行操作
   - PUT: 更新整个资源
   - PATCH: 部分更新资源
   - DELETE: 删除资源

2. 使用有意义的路径命名
3. 返回合适的 HTTP 状态码
4. 保持响应格式一致性

### 数据验证

1. 使用 Pydantic 模型进行请求体验证
2. 使用 FastAPI 的路径参数和查询参数验证功能
3. 对外部输入始终进行验证

### 错误处理

1. 使用 HTTP 状态码表示请求结果
2. 返回有意义的错误信息
3. 对于业务逻辑错误，使用统一的错误响应格式

## 数据存储

当前项目使用内存存储作为示例实现，实际项目中应替换为持久化存储方案，如：
- 关系型数据库（PostgreSQL, MySQL）
- NoSQL 数据库（MongoDB, Redis）
- 其他存储系统

## 部署配置

### 开发环境

使用 docker-compose 运行开发环境，支持热重载：
```bash
docker-compose up
```

### 生产环境

使用 Docker 构建生产镜像，使用 Gunicorn 作为应用服务器：
```bash
docker build -t my-app .
docker run -p 8000:8000 my-app
```

## 代码质量保证

1. 遵循 PEP 8 代码规范
2. 编写适当的注释和文档字符串
3. 确保接口文档的准确性
4. 添加必要的单元测试（虽然当前项目未包含测试目录）

## 常见开发场景

### 添加新的 API 端点

1. 确定端点应属于哪个路由模块
2. 在相应路由文件中添加处理函数
3. 如果需要，创建相应的 Pydantic 模型用于数据验证
4. 如果业务逻辑复杂，将其委托给服务层

### 扩展现有功能

1. 分析现有代码结构
2. 确定需要修改的文件
3. 如果业务逻辑需要扩展，在服务层添加新功能
4. 在路由层添加新的端点或修改现有端点

## 注意事项

1. 不要直接在路由处理函数中实现复杂业务逻辑
2. 保持路由和业务逻辑的分离
3. 确保数据验证和错误处理的一致性
4. 遵循现有的代码风格和命名约定
5. 添加适当的文档注释