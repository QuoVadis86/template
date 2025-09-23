from fastapi import APIRouter
from models import ResponseModel
from utils import success_response, error_response, api_response

router = APIRouter()

# 模拟内存存储（实际中可能是与调度器核心通信）
tasks_db = {}

@router.post("/", response_model=ResponseModel)
@api_response
async def create_task(task_config: dict):
    """接收任务配置，直接返回任务ID"""
    task_id = f"task_{len(tasks_db) + 1}"
    tasks_db[task_id] = task_config
    return {"task_id": task_id, "status": "created"}

@router.get("/{task_id}", response_model=ResponseModel)
@api_response
async def get_task_status(task_id: str):
    """获取任务状态"""
    if task_id not in tasks_db:
        return error_response(
            error="task not found",
            message="任务不存在",
            code=404
        )
    return {"task_id": task_id, "status": "running", "config": tasks_db[task_id]}

@router.post("/{task_id}/stop", response_model=ResponseModel)
@api_response
async def stop_task(task_id: str):
    """停止指定任务"""
    if task_id in tasks_db:
        return {"task_id": task_id, "status": "stopped"}
    return error_response(
        error="task not found",
        message="任务不存在",
        code=404
    )

@router.get("/", response_model=ResponseModel)
@api_response
async def list_all_tasks():
    """列出所有任务"""
    return {"tasks": list(tasks_db.keys())}
