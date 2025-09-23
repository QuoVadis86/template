from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.browser_service import BrowserService
from utils import api_response

router = APIRouter()
browser_service = BrowserService()


class CookieUpdateRequest(BaseModel):
    cookie: str


class UserAgentUpdateRequest(BaseModel):
    user_agent: str


@router.post("/cookie", response_model=dict)
@api_response
async def update_cookie(request: CookieUpdateRequest):
    """更新cookie配置"""
    browser_service.set_cookie(request.cookie)
    return {"message": "Cookie已更新"}


@router.post("/user-agent", response_model=dict)
@api_response
async def update_user_agent(request: UserAgentUpdateRequest):
    """更新用户代理配置"""
    browser_service.set_user_agent(request.user_agent)
    return {"message": "User-Agent已更新"}


@router.get("/status", response_model=dict)
@api_response
async def check_login_status():
    """检测登录状态是否过期"""
    status = browser_service.check_login_status()
    return status