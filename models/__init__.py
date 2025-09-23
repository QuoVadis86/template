from pydantic import BaseModel
from typing import Optional, Any

class ResponseModel(BaseModel):
    """通用响应模型"""
    code: int = 200
    message: str = "success"
    data: Optional[Any] = None
    error: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "code": 200,
                "message": "success",
                "data": None,
                "error": None
            }
        }

class ErrorResponseModel(BaseModel):
    """错误响应模型"""
    code: int = 500
    message: str = "error"
    data: Optional[Any] = None
    error: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "code": 500,
                "message": "error",
                "data": None,
                "error": "错误详情"
            }
        }