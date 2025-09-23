from fastapi import APIRouter
from models import ResponseModel
from utils import success_response, error_response

router = APIRouter()

# 节点状态缓存
nodes_status = {
    "node_1": {"status": "active", "load": 0.3},
    "node_2": {"status": "active", "load": 0.8},
    "node_3": {"status": "offline", "load": 0.0}
}

@router.get("/", response_model=ResponseModel)
async def get_nodes_status():
    """获取所有节点状态"""
    return success_response(
        data=nodes_status,
        message="获取节点状态成功"
    )

@router.get("/{node_id}", response_model=ResponseModel)
async def get_node_status(node_id: str):
    """获取特定节点状态"""
    if node_id in nodes_status:
        return success_response(
            data=nodes_status[node_id],
            message="获取节点状态成功"
        )
    return error_response(
        error="node not found",
        message="节点不存在",
        code=404
    )

@router.post("/{node_id}/drain", response_model=ResponseModel)
async def drain_node(node_id: str):
    """将节点设置为排水模式（不再接收新任务）"""
    if node_id in nodes_status:
        nodes_status[node_id]["status"] = "draining"
        return success_response(
            data={"node_id": node_id, "status": "draining"},
            message="节点已设置为排水模式"
        )
    return error_response(
        error="node not found",
        message="节点不存在",
        code=404
    )