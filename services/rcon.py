import os
from mcrcon import MCRcon
from typing import Optional, Union, List

class MinecraftRcon:
    """
    Minecraft RCON客户端封装类
    提供完整的服务器管理功能
    """
    
    def __init__(self, host: str = "localhost", password: str = "password", port: int = 25575):
        """
        初始化RCON连接参数
        
        Args:
            host: 服务器地址
            password: RCON密码
            port: RCON端口
        """
        self.host = os.getenv("RCON_HOST", host)
        self.password = os.getenv("RCON_PASSWORD", password)
        self.port = int(os.getenv("RCON_PORT", port))
    
    def _connect(self) -> MCRcon:
        """
        内部方法：创建并返回RCON连接实例
        
        Returns:
            MCRcon: 连接实例
        """
        return MCRcon(self.host, self.password, self.port)
    
    def _execute_command(self, command: str) -> str:
        """
        内部方法：执行RCON命令
        
        Args:
            command: 要执行的命令
            
        Returns:
            str: 命令执行结果
        """
        try:
            with self._connect() as mcr:
                return mcr.command(command)
        except Exception as e:
            return f"执行命令失败: {e}"
    
    # ==================== 玩家管理 ====================
    
    def list_players(self) -> str:
        """
        获取在线玩家列表
        
        Returns:
            str: 玩家列表信息
        """
        return self._execute_command("list")
    
    def send_broadcast(self, message: str) -> str:
        """
        向所有玩家发送广播消息
        
        Args:
            message: 要发送的消息
            
        Returns:
            str: 执行结果
        """
        return self._execute_command(f"say {message}")
    
    def send_custom_broadcast(self, sender: str, message: str) -> str:
        """
        向所有玩家发送自定义发送者名称的广播消息
        
        Args:
            sender: 发送者名称
            message: 要发送的消息
            
        Returns:
            str: 执行结果
        """
        return self._execute_command(f"tellraw @a {{\"text\":\"<{sender}> {message}\"}}")
    
    def send_private_message(self, player: str, message: str) -> str:
        """
        向指定玩家发送私信
        
        Args:
            player: 玩家名称
            message: 要发送的消息
            
        Returns:
            str: 执行结果
        """
        return self._execute_command(f"tell {player} {message}")
    
    def kick_player(self, player: str, reason: str = "") -> str:
        """
        踢出玩家
        
        Args:
            player: 玩家名称
            reason: 踢出原因（可选）
            
        Returns:
            str: 执行结果
        """
        if reason:
            return self._execute_command(f"kick {player} {reason}")
        else:
            return self._execute_command(f"kick {player}")
    
    def ban_player(self, player: str, reason: str = "") -> str:
        """
        封禁玩家
        
        Args:
            player: 玩家名称
            reason: 封禁原因（可选）
            
        Returns:
            str: 执行结果
        """
        if reason:
            return self._execute_command(f"ban {player} {reason}")
        else:
            return self._execute_command(f"ban {player}")
    
    def pardon_player(self, player: str) -> str:
        """
        解除玩家封禁
        
        Args:
            player: 玩家名称
            
        Returns:
            str: 执行结果
        """
        return self._execute_command(f"pardon {player}")
    
    def ban_ip(self, ip: str) -> str:
        """
        封禁IP地址
        
        Args:
            ip: IP地址
            
        Returns:
            str: 执行结果
        """
        return self._execute_command(f"ban-ip {ip}")
    
    def pardon_ip(self, ip: str) -> str:
        """
        解除IP封禁
        
        Args:
            ip: IP地址
            
        Returns:
            str: 执行结果
        """
        return self._execute_command(f"pardon-ip {ip}")
    
    # ==================== 物品与经济 ====================
    
    def give_item(self, player: str, item: str, count: int = 1, data: int = 0) -> str:
        """
        给予玩家物品
        
        Args:
            player: 玩家名称
            item: 物品ID或名称
            count: 数量（默认为1）
            data: 数据值（默认为0）
            
        Returns:
            str: 执行结果
        """
        return self._execute_command(f"give {player} {item} {count} {data}")
    
    def clear_inventory(self, player: str, item: str = "", count: int = -1) -> str:
        """
        清空玩家物品栏
        
        Args:
            player: 玩家名称
            item: 物品ID或名称（可选，为空则清空所有）
            count: 清空数量（-1表示全部）
            
        Returns:
            str: 执行结果
        """
        if item:
            return self._execute_command(f"clear {player} {item} {count}")
        else:
            return self._execute_command(f"clear {player}")
    
    # ==================== 传送系统 ====================
    
    def teleport(self, player: str, target: str) -> str:
        """
        传送玩家到目标位置或其他玩家
        
        Args:
            player: 要传送的玩家
            target: 目标位置或玩家
            
        Returns:
            str: 执行结果
        """
        return self._execute_command(f"tp {player} {target}")
    
    def teleport_to_coordinates(self, player: str, x: float, y: float, z: float) -> str:
        """
        传送玩家到指定坐标
        
        Args:
            player: 要传送的玩家
            x: X坐标
            y: Y坐标
            z: Z坐标
            
        Returns:
            str: 执行结果
        """
        return self._execute_command(f"tp {player} {x} {y} {z}")
    
    def teleport_with_rotation(self, player: str, x: float, y: float, z: float, yaw: float, pitch: float) -> str:
        """
        传送玩家到指定坐标并设置视角
        
        Args:
            player: 要传送的玩家
            x: X坐标
            y: Y坐标
            z: Z坐标
            yaw: 偏航角
            pitch: 俯仰角
            
        Returns:
            str: 执行结果
        """
        return self._execute_command(f"tp {player} {x} {y} {z} {yaw} {pitch}")
    
    # ==================== 世界控制 ====================
    
    def set_time(self, time: Union[int, str]) -> str:
        """
        设置游戏时间
        
        Args:
            time: 时间值（数字或关键字如'day', 'night'）
            
        Returns:
            str: 执行结果
        """
        return self._execute_command(f"time set {time}")
    
    def add_time(self, time: int) -> str:
        """
        增加游戏时间
        
        Args:
            time: 要增加的时间值
            
        Returns:
            str: 执行结果
        """
        return self._execute_command(f"time add {time}")
    
    def set_weather(self, weather: str, duration: int = 0) -> str:
        """
        设置天气
        
        Args:
            weather: 天气类型 ('clear', 'rain', 'thunder')
            duration: 持续时间（秒，默认为0表示使用默认持续时间）
            
        Returns:
            str: 执行结果
        """
        if duration > 0:
            return self._execute_command(f"weather {weather} {duration}")
        else:
            return self._execute_command(f"weather {weather}")
    
    def set_world_difficulty(self, difficulty: str) -> str:
        """
        设置游戏难度
        
        Args:
            difficulty: 难度等级 ('peaceful', 'easy', 'normal', 'hard')
            
        Returns:
            str: 执行结果
        """
        return self._execute_command(f"difficulty {difficulty}")
    
    def set_game_mode(self, player: str, mode: str) -> str:
        """
        设置玩家游戏模式
        
        Args:
            player: 玩家名称
            mode: 游戏模式 ('survival', 'creative', 'adventure', 'spectator')
            
        Returns:
            str: 执行结果
        """
        return self._execute_command(f"gamemode {mode} {player}")
    
    # ==================== 服务器管理 ====================
    
    def save_all(self) -> str:
        """
        保存所有世界数据
        
        Returns:
            str: 执行结果
        """
        return self._execute_command("save-all")
    
    def save_on(self) -> str:
        """
        启用自动保存
        
        Returns:
            str: 执行结果
        """
        return self._execute_command("save-on")
    
    def save_off(self) -> str:
        """
        禁用自动保存
        
        Returns:
            str: 执行结果
        """
        return self._execute_command("save-off")
    
    def stop_server(self) -> str:
        """
        停止服务器
        
        Returns:
            str: 执行结果
        """
        return self._execute_command("stop")
    
    def reload_whitelist(self) -> str:
        """
        重新加载白名单
        
        Returns:
            str: 执行结果
        """
        return self._execute_command("whitelist reload")
    
    def add_to_whitelist(self, player: str) -> str:
        """
        添加玩家到白名单
        
        Args:
            player: 玩家名称
            
        Returns:
            str: 执行结果
        """
        return self._execute_command(f"whitelist add {player}")
    
    def remove_from_whitelist(self, player: str) -> str:
        """
        从白名单移除玩家
        
        Args:
            player: 玩家名称
            
        Returns:
            str: 执行结果
        """
        return self._execute_command(f"whitelist remove {player}")
    
    def list_whitelist(self) -> str:
        """
        列出白名单玩家
        
        Returns:
            str: 白名单列表
        """
        return self._execute_command("whitelist list")
    
    def enable_whitelist(self) -> str:
        """
        启用白名单
        
        Returns:
            str: 执行结果
        """
        return self._execute_command("whitelist on")
    
    def disable_whitelist(self) -> str:
        """
        禁用白名单
        
        Returns:
            str: 执行结果
        """
        return self._execute_command("whitelist off")

# 使用示例
if __name__ == "__main__":
    # 创建RCON客户端实例
    rcon = MinecraftRcon("localhost", "password", 25575)
    
    # 玩家管理示例
    print("在线玩家:", rcon.list_players())
    print("发送广播:", rcon.send_broadcast("Hello from Python!"))
    print("私信玩家:", rcon.send_private_message("Steve", "This is a private message"))
    
    # 物品管理示例
    print("给予物品:", rcon.give_item("Steve", "diamond", 5))
    
    # 传送示例
    print("传送玩家:", rcon.teleport("Steve", "Alex"))
    
    # 世界控制示例
    print("设置时间为白天:", rcon.set_time("day"))
    print("设置晴天:", rcon.set_weather("clear"))
    
    # 服务器管理示例
    print("保存世界:", rcon.save_all())