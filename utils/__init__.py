from models import ResponseModel, ErrorResponseModel
from typing import Any, Callable
from functools import wraps

def success_response(data: Any = None, message: str = "success", code: int = 200) -> ResponseModel:
    """
    创建成功的响应
    
    Args:
        data: 返回的数据
        message: 响应消息
        code: 响应码
        
    Returns:
        ResponseModel: 成功响应模型
    """
    return ResponseModel(
        code=code,
        message=message,
        data=data
    )

def error_response(error: str = None, message: str = "error", code: int = 500) -> ErrorResponseModel:
    """
    创建错误响应
    
    Args:
        error: 错误详情
        message: 响应消息
        code: 错误码
        
    Returns:
        ErrorResponseModel: 错误响应模型
    """
    return ErrorResponseModel(
        code=code,
        message=message,
        error=error
    )

def api_response(handler_func: Callable) -> Callable:
    """
    装饰器：自动处理API响应格式
    
    成功时返回 success_response
    异常时返回 error_response
    
    Args:
        handler_func: 被装饰的处理函数
        
    Returns:
        装饰后的函数
    """
    @wraps(handler_func)
    async def wrapper(*args, **kwargs):
        try:
            result = await handler_func(*args, **kwargs)
            # 如果函数返回的是 ResponseModel 或 ErrorResponseModel，直接返回
            if isinstance(result, (ResponseModel, ErrorResponseModel)):
                return result
            # 否则自动包装为成功响应
            return success_response(data=result)
        except Exception as e:
            return error_response(error=str(e))
    return wrapper