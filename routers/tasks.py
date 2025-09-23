from fastapi import APIRouter, HTTPException
from models import ResponseModel
from utils import api_response
from services.tasks import TaskService

router = APIRouter()
task_service = TaskService()

@router.post("/", response_model=ResponseModel)
@api_response
async def create_task(task_config: dict):
    """接收任务配置，直接返回任务ID"""
    return task_service.create_task(task_config)

@router.get("/{task_id}", response_model=ResponseModel)
@api_response
async def get_task_status(task_id: str):
    """获取任务状态"""
    try:
        return task_service.get_task_status(task_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="任务不存在")

@router.post("/{task_id}/stop", response_model=ResponseModel)
@api_response
async def stop_task(task_id: str):
    """停止指定任务"""
    try:
        return task_service.stop_task(task_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="任务不存在")

@router.get("/", response_model=ResponseModel)
@api_response
async def list_all_tasks():
    """列出所有任务"""
    return task_service.list_all_tasks()