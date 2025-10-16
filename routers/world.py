from fastapi import APIRouter, HTTPException

from models import ResponseModel
from utils import api_response
from services.rcon import MinecraftRcon
from models.minecraft import *

router = APIRouter()
rcon = MinecraftRcon()


@router.post("/time", response_model=ResponseModel)
@api_response
async def set_time(time_setting: TimeSetting):
    """设置游戏时间"""
    result = rcon.set_time(time_setting.time)
    return result


@router.post("/weather", response_model=ResponseModel)
@api_response
async def set_weather(weather_setting: WeatherSetting):
    """设置天气"""
    if weather_setting.duration is not None:
        result = rcon.set_weather(weather_setting.weather, weather_setting.duration)
    else:
        result = rcon.set_weather(weather_setting.weather)
    return result


@router.post("/save", response_model=ResponseModel)
@api_response
async def save_all():
    """保存所有世界数据"""
    result = rcon.save_all()
    return result