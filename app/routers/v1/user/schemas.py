from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[str] = None

# 用户注册模型
class UserCreate(BaseModel):
    username: str
    full_name: Optional[str] = None  # 可选字段
    phone: Optional[str] = None      # 可选字段
    password: str                    # 密码
    address: Optional[str] = None    # 地址
    city: Optional[str] = None       # 城市
    country: Optional[str] = None    # 国家
    postal_code: Optional[str] = None  # 邮政编码
    date_of_birth: Optional[date] = None  # 生日
    gender: Optional[str] = None     # 性别
    avatar_url: Optional[str] = None  # 头像 URL

class UserLogin(BaseModel):
    username: str
    password: str                    # 密码

# 用户响应模型
class UserResponse(BaseModel):
    id: str
    username: str
    full_name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    avatar_url: Optional[str] = None
    is_active: bool
    created_at: date

    class Config:
        orm_mode = True  # 允许 ORM 模型直接转换为 Pydantic 模型