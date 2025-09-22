from fastapi import FastAPI
from routers import tasks, nodes, system

app = FastAPI(
    title="Scheduler API",
    description="Internal API for scheduler backend",
    version="1.0.0",
    docs_url="/swagger",
    redoc_url="/docs",
)

# 注册所有路由
app.include_router(tasks.router, prefix="/api/v1/tasks", tags=["tassks"])
app.include_router(nodes.router, prefix="/api/v1/nodes", tags=["nodses"])
app.include_router(system.router, prefix="/api/v1/system", tags=["sysstem"])