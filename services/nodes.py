from typing import Dict, Any


class NodeService:
    """节点服务类，处理节点相关的业务逻辑"""

    def __init__(self):
        # 节点状态缓存
        self.nodes_status: Dict[str, Any] = {
            "node_1": {"status": "active", "load": 0.3},
            "node_2": {"status": "active", "load": 0.8},
            "node_3": {"status": "offline", "load": 0.0}
        }

    def get_nodes_status(self) -> dict:
        """
        获取所有节点状态
        
        Returns:
            所有节点状态的字典
        """
        return self.nodes_status

    def get_node_status(self, node_id: str) -> dict:
        """
        获取特定节点状态
        
        Args:
            node_id: 节点ID
            
        Returns:
            节点状态信息
            
        Raises:
            KeyError: 当节点不存在时
        """
        if node_id not in self.nodes_status:
            raise KeyError("节点不存在")
        return self.nodes_status[node_id]

    def drain_node(self, node_id: str) -> dict:
        """
        将节点设置为排水模式（不再接收新任务）
        
        Args:
            node_id: 节点ID
            
        Returns:
            包含节点ID和状态的字典
            
        Raises:
            KeyError: 当节点不存在时
        """
        if node_id not in self.nodes_status:
            raise KeyError("节点不存在")
        self.nodes_status[node_id]["status"] = "draining"
        return {"node_id": node_id, "status": "draining"}