# 服务层设计文档

## 概述

本文档详细描述了项目中服务层的结构设计和各服务类的职责。服务层遵循单一职责原则，每个服务类负责特定的业务功能。

## 服务层结构

```
services/
├── config_service.py        # 配置管理服务
├── messaging_service.py     # 消息服务（私信功能）
├── player_service.py        # 玩家信息服务
├── job_service.py           # 差事信息服务
└── __init__.py
```

## 详细设计

### 1. ConfigService - 配置管理服务

负责处理配置管理相关的业务逻辑。

#### 主要功能
- 管理用户 cookie 配置
- 检测登录状态是否过期
- 提供配置相关的工具方法

#### 接口设计
```python
class ConfigService:
    def set_cookie(self, cookie: str) -> None:
        """设置用户 cookie"""
        pass
    
    def get_cookie(self) -> str:
        """获取当前用户 cookie"""
        pass
    
    def check_login_status(self) -> dict:
        """检测登录状态是否过期"""
        pass
    
    def save_config(self) -> None:
        """保存配置到文件"""
        pass
    
    def load_config(self) -> None:
        """从文件加载配置"""
        pass
```

### 2. MessagingService - 消息服务

负责处理消息发送相关的业务逻辑。

#### 主要功能
- 发送私信给指定好友
- 管理消息历史记录

#### 接口设计
```python
class MessagingService:
    def send_message(self, recipient: str, message: str) -> dict:
        """发送私信给指定好友"""
        pass
    
    def get_message_history(self, recipient: str) -> list:
        """获取与指定好友的消息历史"""
        pass
```

### 3. PlayerService - 玩家信息服务

负责处理玩家信息查询相关的业务逻辑。

#### 主要功能
- 搜索玩家
- 获取玩家详细信息

#### 接口设计
```python
class PlayerService:
    def search_player(self, query: str) -> list:
        """根据查询条件搜索玩家"""
        pass
    
    def get_player_info(self, player_id: str) -> dict:
        """获取指定玩家的详细信息"""
        pass
```

### 4. JobService - 差事信息服务

负责处理差事信息获取相关的业务逻辑。

#### 主要功能
- 根据差事代码获取差事信息
- 解析差事页面内容

#### 接口设计
```python
class JobService:
    def get_job_info(self, job_code: str) -> dict:
        """根据差事代码获取差事信息"""
        pass
    
    def search_jobs(self, query: str) -> list:
        """搜索差事"""
        pass
```

## 服务依赖关系

```
ConfigService (基础服务)
    ├── MessagingService (依赖配置)
    ├── PlayerService (依赖配置)
    └── JobService (依赖配置)
```

所有服务都需要 ConfigService 提供的配置信息来执行需要登录的操作。

## 配置管理

服务层将使用配置文件来存储和管理用户 cookie，支持 Docker 挂载：

### 配置文件格式 (config.json)
```json
{
  "cookie": "用户提供的完整 cookie 字符串",
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