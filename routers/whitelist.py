from fastapi import APIRouter, HTTPException

from models import ResponseModel
from utils import api_response
from services.rcon import MinecraftRcon
from models.minecraft import WhitelistAction

router = APIRouter()
rcon = MinecraftRcon()


@router.post("/add", response_model=ResponseModel)
@api_response
async def add_to_whitelist(player_data: WhitelistAction):
    """添加玩家到白名单"""
    result = rcon.add_to_whitelist(player_data.player)
    return result


@router.post("/remove", response_model=ResponseModel)
@api_response
async def remove_from_whitelist(player_data: WhitelistAction):
    """从白名单移除玩家"""
    result = rcon.remove_from_whitelist(player_data.player)
    return result


@router.get("/list", response_model=ResponseModel)
@api_response
async def list_whitelist():
    """列出白名单玩家"""
    result = rcon.list_whitelist()
    return result