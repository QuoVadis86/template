from typing import Dict, Any


class TaskService:
    """任务服务类，处理任务相关的业务逻辑"""

    def __init__(self):
        # 模拟内存存储（实际中可能是与调度器核心通信）
        self.tasks_db: Dict[str, Any] = {}

    def create_task(self, task_config: dict) -> dict:
        """
        创建任务
        
        Args:
            task_config: 任务配置
            
        Returns:
            包含任务ID和状态的字典
        """
        task_id = f"task_{len(self.tasks_db) + 1}"
        self.tasks_db[task_id] = task_config
        return {"task_id": task_id, "status": "created"}

    def get_task_status(self, task_id: str) -> dict:
        """
        获取任务状态
        
        Args:
            task_id: 任务ID
            
        Returns:
            包含任务状态和配置的字典
            
        Raises:
            KeyError: 当任务不存在时
        """
        if task_id not in self.tasks_db:
            raise KeyError("任务不存在")
        return {"task_id": task_id, "status": "running", "config": self.tasks_db[task_id]}

    def stop_task(self, task_id: str) -> dict:
        """
        停止指定任务
        
        Args:
            task_id: 任务ID
            
        Returns:
            包含任务ID和状态的字典
            
        Raises:
            KeyError: 当任务不存在时
        """
        if task_id not in self.tasks_db:
            raise KeyError("任务不存在")
        return {"task_id": task_id, "status": "stopped"}

    def list_all_tasks(self) -> dict:
        """
        列出所有任务
        
        Returns:
            包含任务列表的字典
        """
        return {"tasks": list(self.tasks_db.keys())}