from fastapi import APIRouter

router = APIRouter()

# 节点状态缓存
nodes_status = {
    "node_1": {"status": "active", "load": 0.3},
    "node_2": {"status": "active", "load": 0.8},
    "node_3": {"status": "offline", "load": 0.0}
}

@router.get("/")
async def get_nodes_status():
    """获取所有节点状态"""
    return nodes_status

@router.get("/{node_id}")
async def get_node_status(node_id: str):
    """获取特定节点状态"""
    return nodes_status.get(node_id, {"error": "node not found"})

@router.post("/{node_id}/drain")
async def drain_node(node_id: str):
    """将节点设置为排水模式（不再接收新任务）"""
    if node_id in nodes_status:
        nodes_status[node_id]["status"] = "draining"
        return {"node_id": node_id, "status": "draining"}
    return {"error": "node not found"}