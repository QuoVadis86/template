# 项目需求文档

## 概述

本项目需要实现一个基于 Rockstar Social Club 的自动化操作 API 服务。通过用户提供的 cookie 进行身份验证，实现一系列自动化操作功能。

## 功能需求

### 1. 配置管理
- 将用户提供的 cookie 保存到本地配置文件中
- 支持 Docker 挂载配置文件以便修改
- 提供接口检测登录状态是否过期

### 2. 好友私信功能
- 提供 API 接口用于给指定好友发送私信
- 需要能够指定接收者和消息内容

### 3. 玩家搜索功能
- 提供 API 接口用于搜索指定玩家
- 获取并返回玩家的详细信息

### 4. 差事信息获取功能
- 根据差事代码构建访问地址: https://socialclub.rockstargames.com/job/gtav/{差事代码}
- 例如: https://socialclub.rockstargames.com/job/gtav/Ae6dRykqOUCmd7UMavUWng
- 获取并解析页面信息，返回结构化数据

## 技术要求

### 服务层设计
```
services/
├── browser_service.py       # 浏览器上下文服务（核心服务）
├── messaging_service.py     # 消息服务（私信功能）
├── player_service.py        # 玩家信息服务
├── job_service.py           # 差事信息服务
└── __init__.py
```

### 路由层设计
```
routers/
├── browser.py               # 浏览器上下文相关路由
├── messages.py              # 消息相关路由
├── players.py               # 玩家相关路由
├── jobs.py                  # 差事相关路由
└── __init__.py
```

### 配置文件设计
配置文件应支持 Docker 挂载，存储在项目根目录下的 `config.json` 文件中:
```json
{
  "cookie": "用户提供的完整 cookie 字符串",
  "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
  "last_updated": "2023-01-01T00:00:00Z"
}
```

### 主要依赖
- HTTP 客户端用于发送请求和处理 cookie
- HTML 解析库用于解析页面信息
- 配置管理模块用于存储和读取 cookie

## 数据结构设计

### 1. 玩家信息结构
```json
{
  "player_id": "string",
  "username": "string",
  "avatar": "string",
  "status": "string",
  "last_active": "datetime"
}
```

### 2. 差事信息结构
```json
{
  "job_id": "string",
  "title": "string",
  "description": "string",
  "creator": "string",
  "rating": "number",
  "downloads": "number"
}
```

### 3. 消息结构
```json
{
  "recipient": "string",
  "message": "string",
  "timestamp": "datetime"
}
```

### 4. 登录状态结构
```json
{
  "is_logged_in": "boolean",
  "expires_in": "number"
}
```