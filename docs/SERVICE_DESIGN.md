# 服务层设计文档

## 概述

本文档详细描述了项目中服务层的结构设计和各服务类的职责。服务层遵循单一职责原则，每个服务类负责特定的业务功能。

## 服务层结构

```
services/
├── browser_service.py       # 浏览器上下文服务（核心服务）
├── messaging_service.py     # 消息服务（私信功能）
├── player_service.py        # 玩家信息服务
├── job_service.py           # 差事信息服务
└── __init__.py
```

## 详细设计

### 1. BrowserService - 浏览器上下文服务

负责管理共享的浏览器上下文，包括cookie、用户代理等信息，是所有其他服务的基础。

#### 主要功能
- 管理HTTP客户端实例
- 维护会话状态（cookie、用户代理等）
- 提供通用的HTTP请求方法
- 检测登录状态是否过期

#### 接口设计
```python
class BrowserService:
    def __init__(self, config_path: str = "config.json"):
        """初始化浏览器服务"""
        pass
    
    def get_client(self) -> httpx.Client:
        """获取HTTP客户端实例"""
        pass
    
    def set_cookie(self, cookie: str) -> None:
        """设置用户 cookie"""
        pass
    
    def get_cookie(self) -> str:
        """获取当前用户 cookie"""
        pass
    
    def set_user_agent(self, user_agent: str) -> None:
        """设置用户代理"""
        pass
    
    def get_user_agent(self) -> str:
        """获取当前用户代理"""
        pass
    
    def check_login_status(self) -> dict:
        """检测登录状态是否过期"""
        pass
    
    def request(self, method: str, url: str, **kwargs) -> httpx.Response:
        """发送HTTP请求"""
        pass
    
    def save_config(self) -> None:
        """保存配置到文件"""
        pass
    
    def load_config(self) -> None:
        """从文件加载配置"""
        pass
```

### 2. MessagingService - 消息服务

负责处理消息发送相关的业务逻辑，依赖BrowserService提供的HTTP客户端。

#### 主要功能
- 发送私信给指定好友
- 管理消息历史记录

#### 接口设计
```python
class MessagingService:
    def __init__(self, browser_service: BrowserService):
        """初始化消息服务"""
        pass
    
    def send_message(self, recipient: str, message: str) -> dict:
        """发送私信给指定好友"""
        pass
    
    def get_message_history(self, recipient: str) -> list:
        """获取与指定好友的消息历史"""
        pass
```

### 3. PlayerService - 玩家信息服务

负责处理玩家信息查询相关的业务逻辑，依赖BrowserService提供的HTTP客户端。

#### 主要功能
- 搜索玩家
- 获取玩家详细信息

#### 接口设计
```python
class PlayerService:
    def __init__(self, browser_service: BrowserService):
        """初始化玩家信息服务"""
        pass
    
    def search_player(self, query: str) -> list:
        """根据查询条件搜索玩家"""
        pass
    
    def get_player_info(self, player_id: str) -> dict:
        """获取指定玩家的详细信息"""
        pass
```

### 4. JobService - 差事信息服务

负责处理差事信息获取相关的业务逻辑，依赖BrowserService提供的HTTP客户端。

#### 主要功能
- 根据差事代码获取差事信息
- 解析差事页面内容

#### 接口设计
```python
class JobService:
    def __init__(self, browser_service: BrowserService):
        """初始化差事信息服务"""
        pass
    
    def get_job_info(self, job_code: str) -> dict:
        """根据差事代码获取差事信息"""
        pass
    
    def search_jobs(self, query: str) -> list:
        """搜索差事"""
        pass
```

## 服务依赖关系

```
BrowserService (核心服务)
    ├── MessagingService (依赖浏览器服务)
    ├── PlayerService (依赖浏览器服务)
    └── JobService (依赖浏览器服务)
```

所有服务都需要 BrowserService 提供的HTTP客户端和认证信息来执行需要登录的操作。

## 配置管理

服务层将使用配置文件来存储和管理用户 cookie，支持 Docker 挂载：

### 配置文件格式 (config.json)
```json
{
  "cookie": "用户提供的完整 cookie 字符串",
  "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
  "last_updated": "2023-01-01T00:00:00Z"
}
```

配置文件应存储在项目根目录，以便在 Docker 环境中可以轻松挂载。

## 错误处理

所有服务方法都应该适当处理以下类型的错误：
1. 网络连接错误
2. 认证失败错误（登录过期）
3. 资源未找到错误
4. 解析错误
5. 服务器错误

错误应该通过抛出适当的异常或返回错误信息来处理，而不是直接处理 HTTP 错误响应。