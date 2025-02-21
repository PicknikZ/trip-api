from fastapi import Depends, Request, HTTPException
from app.models import UserProfile

def get_current_user(request: Request) -> UserProfile:
    """
    从请求上下文中获取当前用户。
    """
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=401, detail="User not authenticated")
    return user