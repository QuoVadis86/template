from fastapi import APIRouter
from models import ResponseModel
from utils import api_response

router = APIRouter()

@router.get("/health", response_model=ResponseModel)
@api_response
async def health_check():
    """健康检查端点"""
    return {"status": "healthy", "timestamp": "2024-01-01T12:00:00Z"}

@router.get("/metrics", response_model=ResponseModel)
@api_response
async def get_metrics():
    """获取系统指标"""
    metrics_data = {
        "active_connections": 42,
        "memory_usage": "1.2GB",
        "uptime": "12h 34m"
    }
    return metrics_data

@router.post("/restart", response_model=ResponseModel)
@api_response
async def restart_service():
    """重启服务（实际实现会有更复杂的逻辑）"""
    return {"status": "restarting", "message": "Service will restart shortly"}