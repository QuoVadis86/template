from fastapi import FastAPI
from routers import config

app = FastAPI(
    title="Scheduler API",
    description="Internal API for scheduler backend",
    version="1.0.0",
    docs_url="/swagger",
    redoc_url="/docs",
)

# 注册所有路由
app.include_router(config.router, prefix="/api/v1/config", tags=["config"])

# uvicorn main:app --reload --port 5000