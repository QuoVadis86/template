from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.config_service import ConfigService
from utils import api_response

router = APIRouter()
config_service = ConfigService()


class CookieUpdateRequest(BaseModel):
    cookie: str


class LoginStatusResponse(BaseModel):
    is_logged_in: bool
    error: str = None


@router.post("/cookie", response_model=dict)
@api_response
async def update_cookie(request: CookieUpdateRequest):
    """更新cookie配置"""
    config_service.set_cookie(request.cookie)
    return {"message": "Cookie已更新"}


@router.get("/status", response_model=dict)
@api_response
async def check_login_status():
    """检测登录状态是否过期"""
    status = config_service.check_login_status()
    return status