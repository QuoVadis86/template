from models import ResponseModel, ErrorResponseModel
from typing import Any

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