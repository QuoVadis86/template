from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from routers import player, world, whitelist

app = FastAPI(
    title="Scheduler API",
    description="Internal API for scheduler backend",
    version="1.0.0",
    docs_url="/swagger",
    redoc_url="/docs",
)

# 注册所有路由
app.include_router(player.router, prefix="/api/v1/player", tags=["player"])
app.include_router(world.router, prefix="/api/v1/world", tags=["world"])
app.include_router(whitelist.router, prefix="/api/v1/whitelist", tags=["whitelist"])


@app.get("/", include_in_schema=False)
async def redirect_to_swagger():
    """根路径重定向到Swagger UI"""
    return RedirectResponse(url="/swagger")


# uvicorn main:app --reload --port 5000