from fastapi import APIRouter
from models import ResponseModel
from utils import success_response, error_response

router = APIRouter()

# 模拟内存存储（实际中可能是与调度器核心通信）
tasks_db = {}

@router.post("/", response_model=ResponseModel)
async def create_task(task_config: dict):
    """接收任务配置，直接返回任务ID"""
    try:
        task_id = f"task_{len(tasks_db) + 1}"
        tasks_db[task_id] = task_config
        return success_response(
            data={"task_id": task_id, "status": "created"},
            message="任务创建成功"
        )
    except Exception as e:
        return error_response(
            error=str(e),
            message="任务创建失败"
        )

@router.get("/{task_id}", response_model=ResponseModel)
async def get_task_status(task_id: str):
    """获取任务状态"""
    if task_id not in tasks_db:
        return error_response(
            error="task not found",
            message="任务不存在",
            code=404
        )
    return success_response(
        data={"task_id": task_id, "status": "running", "config": tasks_db[task_id]},
        message="获取任务状态成功"
    )

@router.post("/{task_id}/stop", response_model=ResponseModel)
async def stop_task(task_id: str):
    """停止指定任务"""
    if task_id in tasks_db:
        return success_response(
            data={"task_id": task_id, "status": "stopped"},
            message="任务已停止"
        )
    return error_response(
        error="task not found",
        message="任务不存在",
        code=404
    )

@router.get("/", response_model=ResponseModel)
async def list_all_tasks():
    """列出所有任务"""
    return success_response(
        data={"tasks": list(tasks_db.keys())},
        message="获取任务列表成功"
    )