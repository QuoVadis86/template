from fastapi import APIRouter
from models import ResponseModel
from utils import success_response, error_response

router = APIRouter()

@router.get("/health", response_model=ResponseModel)
async def health_check():
    """健康检查端点"""
    return success_response(
        data={"status": "healthy", "timestamp": "2024-01-01T12:00:00Z"},
        message="服务运行正常"
    )

@router.get("/metrics", response_model=ResponseModel)
async def get_metrics():
    """获取系统指标"""
    metrics_data = {
        "active_connections": 42,
        "memory_usage": "1.2GB",
        "uptime": "12h 34m"
    }
    return success_response(
        data=metrics_data,
        message="获取系统指标成功"
    )

@router.post("/restart", response_model=ResponseModel)
async def restart_service():
    """重启服务（实际实现会有更复杂的逻辑）"""
    return success_response(
        data={"status": "restarting", "message": "Service will restart shortly"},
        message="服务正在重启"
    )