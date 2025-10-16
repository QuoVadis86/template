# 请求模型定义

from pydantic import BaseModel
from typing import Optional


class BroadcastMessage(BaseModel):
    message: str


class PrivateMessage(BroadcastMessage):
    player: str


class GiveItem(BaseModel):
    player: str
    item: str
    count: int = 1
    data: int = 0


class Teleport(BaseModel):
    player: str
    target: str


class TeleportCoordinates(BaseModel):
    player: str
    x: float
    y: float
    z: float
    yaw: Optional[float] = None
    pitch: Optional[float] = None


class TimeSetting(BaseModel):
    time: str


class WeatherSetting(BaseModel):
    weather: str
    duration: Optional[int] = None


class GameModeSetting(BaseModel):
    player: str
    mode: str


class KickBanPlayer(BaseModel):
    player: str
    reason: Optional[str] = None


class WhitelistAction(BaseModel):
    player: str
