from fastapi import APIRouter, HTTPException
from models import ResponseModel
from utils import api_response
from services.nodes import NodeService

router = APIRouter()
node_service = NodeService()

@router.get("/", response_model=ResponseModel)
@api_response
async def get_nodes_status():
    """获取所有节点状态"""
    return node_service.get_nodes_status()

@router.get("/{node_id}", response_model=ResponseModel)
@api_response
async def get_node_status(node_id: str):
    """获取特定节点状态"""
    try:
        return node_service.get_node_status(node_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="节点不存在")

@router.post("/{node_id}/drain", response_model=ResponseModel)
@api_response
async def drain_node(node_id: str):
    """将节点设置为排水模式（不再接收新任务）"""
    try:
        return node_service.drain_node(node_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="节点不存在")