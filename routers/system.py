from fastapi import APIRouter
from models import ResponseModel
from utils import api_response
from services.system import SystemService

router = APIRouter()
system_service = SystemService()

@router.get("/health", response_model=ResponseModel)
@api_response
async def health_check():
    """健康检查端点"""
    return system_service.health_check()

@router.get("/metrics", response_model=ResponseModel)
@api_response
async def get_metrics():
    """获取系统指标"""
    return system_service.get_metrics()

@router.post("/restart", response_model=ResponseModel)
@api_response
async def restart_service():
    """重启服务（实际实现会有更复杂的逻辑）"""
    return system_service.restart_service()