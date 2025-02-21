from fastapi import FastAPI
from app.middlewares import AuthMiddleware
from app.database import init_db
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.utils.errors import register_exception_handler
from app.routers.v1.api import router as api_router

# 创建 FastAPI 实例
app = FastAPI()

ALLOWED_HOSTS = settings.ALLOWED_HOSTS
if not ALLOWED_HOSTS:
    ALLOWED_HOSTS = ["*"]

# 添加中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_HOSTS,
    allow_credentials=True if ALLOWED_HOSTS != ["*"] else False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(AuthMiddleware)

register_exception_handler(app)

app.add_event_handler("startup", init_db)
#app.add_event_handler("shutdown")

# 注册路由
app.include_router(api_router, prefix=settings.API_V1_STR)