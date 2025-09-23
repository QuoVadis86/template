import json
import os
from typing import Optional
import httpx


class ConfigService:
    """配置管理服务，处理cookie存储和登录状态检测"""
    
    def __init__(self, config_path: str = "config.json"):
        self.config_path = config_path
        self.cookie: Optional[str] = None
        self.load_config()
    
    def set_cookie(self, cookie: str) -> None:
        """设置用户cookie"""
        self.cookie = cookie
        self.save_config()
    
    def get_cookie(self) -> Optional[str]:
        """获取当前用户cookie"""
        return self.cookie
    
    def check_login_status(self) -> dict:
        """
        检测登录状态是否过期
        
        Returns:
            包含登录状态信息的字典
        """
        if not self.cookie:
            return {"is_logged_in": False, "error": "未设置cookie"}
        
        try:
            # 使用httpx发送请求检测登录状态
            headers = {
                "Cookie": self.cookie,
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            
            # 尝试访问需要登录的页面来检测登录状态
            with httpx.Client() as client:
                response = client.get(
                    "https://socialclub.rockstargames.com/", 
                    headers=headers,
                    follow_redirects=False
                )
                
                # 如果重定向到登录页面，说明登录已过期
                if response.status_code == 302 and "/signin" in response.headers.get("location", ""):
                    return {"is_logged_in": False, "error": "登录已过期"}
                
                # 如果能正常访问，说明登录有效
                if response.status_code == 200:
                    return {"is_logged_in": True, "error": None}
                
                # 其他情况视为登录状态异常
                return {
                    "is_logged_in": False, 
                    "error": f"状态检测异常: {response.status_code}"
                }
                
        except Exception as e:
            return {"is_logged_in": False, "error": str(e)}
    
    def save_config(self) -> None:
        """保存配置到文件"""
        config = {
            "cookie": self.cookie
        }
        
        # 确保目录存在
        os.makedirs(os.path.dirname(self.config_path) if os.path.dirname(self.config_path) else ".", exist_ok=True)
        
        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
    
    def load_config(self) -> None:
        """从文件加载配置"""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    config = json.load(f)
                    self.cookie = config.get("cookie")
            except Exception:
                # 配置文件损坏或格式错误时忽略
                pass