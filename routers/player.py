from fastapi import APIRouter, HTTPException

from models import ResponseModel
from utils import api_response
from services.rcon import MinecraftRcon
from models.minecraft import *

router = APIRouter()
rcon = MinecraftRcon()


@router.get("/list", response_model=ResponseModel)
@api_response
async def list_players():
    """获取在线玩家列表"""
    result = rcon.list_players()
    return result


@router.post("/broadcast", response_model=ResponseModel)
@api_response
async def send_broadcast(message: BroadcastMessage):
    """发送全局消息"""
    result = rcon.send_broadcast(message.message)
    return result


@router.post("/broadcast/custom", response_model=ResponseModel)
@api_response
async def send_custom_broadcast(message: CustomBroadcastMessage):
    """发送自定义发送者名称的全局消息"""
    result = rcon.send_custom_broadcast(message.sender, message.message)
    return result


@router.post("/tell", response_model=ResponseModel)
@api_response
async def send_private_message(pm: PrivateMessage):
    """发送私聊消息"""
    result = rcon.send_private_message(pm.player, pm.message)
    return result


@router.post("/give", response_model=ResponseModel)
@api_response
async def give_item(item_data: GiveItem):
    """给予玩家物品"""
    result = rcon.give_item(item_data.player, item_data.item, item_data.count, item_data.data)
    return result


@router.post("/teleport", response_model=ResponseModel)
@api_response
async def teleport_player(tp: Teleport):
    """传送玩家到另一个玩家或位置"""
    result = rcon.teleport(tp.player, tp.target)
    return result


@router.post("/teleport/coordinates", response_model=ResponseModel)
@api_response
async def teleport_to_coordinates(tp: TeleportCoordinates):
    """传送玩家到指定坐标"""
    if tp.yaw is not None and tp.pitch is not None:
        result = rcon.teleport_with_rotation(tp.player, tp.x, tp.y, tp.z, tp.yaw, tp.pitch)
    else:
        result = rcon.teleport_to_coordinates(tp.player, tp.x, tp.y, tp.z)
    return result


@router.post("/gamemode", response_model=ResponseModel)
@api_response
async def set_game_mode(gamemode_setting: GameModeSetting):
    """设置玩家游戏模式"""
    result = rcon.set_game_mode(gamemode_setting.player, gamemode_setting.mode)
    return result


@router.post("/kick", response_model=ResponseModel)
@api_response
async def kick_player(kick_data: KickBanPlayer):
    """踢出玩家"""
    if kick_data.reason:
        result = rcon.kick_player(kick_data.player, kick_data.reason)
    else:
        result = rcon.kick_player(kick_data.player)
    return result


@router.post("/ban", response_model=ResponseModel)
@api_response
async def ban_player(ban_data: KickBanPlayer):
    """封禁玩家"""
    if ban_data.reason:
        result = rcon.ban_player(ban_data.player, ban_data.reason)
    else:
        result = rcon.ban_player(ban_data.player)
    return result


@router.post("/pardon", response_model=ResponseModel)
@api_response
async def pardon_player(player_data: WhitelistAction):
    """解除封禁玩家"""
    result = rcon.pardon_player(player_data.player)
    return result