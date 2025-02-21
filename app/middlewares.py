from fastapi import Depends, Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy import select
from sqlalchemy.exc import MultipleResultsFound
from jose import JWTError, jwt
from datetime import datetime
from app.database import AsyncSessionLocal
from app.models import UserProfile
from app.config import settings
from app.utils import logger, CommonResponse

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        auth_header = request.headers.get("X-Forwarded-User")
        if not auth_header:
            response = await call_next(request)
            return response

        # 检查是否为 Bearer Token 格式
        if not auth_header.startswith("Bearer "):
            return CommonResponse.failed(status_code=401, err_msg="Invalid token format")
        
        token = auth_header.split(" ")[1]
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            # 检查 Token 是否过期
            expire_time = payload.get("exp")
            if expire_time:
                if datetime.utcnow() > datetime.utcfromtimestamp(expire_time):
                    return CommonResponse.failed(status_code=401, err_msg="Token expired")

            # 提取用户信息
            username = payload.get("username")
            if not username:
                return CommonResponse.failed(status_code=401, err_msg="Invalid token payload")

        except JWTError:
            return CommonResponse.failed(status_code=401, err_msg="Invalid token")


        async with AsyncSessionLocal() as db:
            try:
                res = await db.execute(
                    select(UserProfile)
                    .where(UserProfile.username == username)
                )
                user = res.scalar_one_or_none()  # 结果处理在会话块内
            except MultipleResultsFound:
                # 记录日志并提示数据库数据异常
                logger.error(f"Multiple users found with username: {username}")
                return CommonResponse.failed(status_code=500, err_msg="Data inconsistency error")
            finally:
                await db.close()

        if not user:
            raise CommonResponse.failed(status_code=401, err_msg="User not found")
        # 将用户信息注入到请求上下文中
        request.state.user = user

        # 继续处理请求
        response = await call_next(request)
        return response