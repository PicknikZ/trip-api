from datetime import timedelta
import re
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import UserProfile
from app.services.auth import security
from app.config import settings
from app.services.auth import create_access_token
from app.routers.v1.user.schemas import UserCreate
from app.utils.errors.exceptions import *
from app.utils import logger

class User:
    async def register_user(self, user: UserCreate, db: AsyncSession):
        email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not re.fullmatch(email_regex, user.username):
            raise ServerException(status_code=HTTP_406_NOT_ACCEPTABLE, detail="username {} format not valid".format(user.username))
        
        result = await db.execute(
                          select(UserProfile)
                          .where(UserProfile.username == user.username)
                          )
        user_credentials = result.scalar_one_or_none()
        logger.info(f"user_credentials: {user_credentials}")
        if user_credentials:
            raise ServerException(status_code=HTTP_405_METHOD_NOT_ALLOWED, detail="User {} exists!".format(user.username))
        else:
            hashed_password = security.get_password_hash(user.password)
            # 创建新用户
            db_user = UserProfile(
                username=user.username,
                full_name=user.full_name,
                phone=user.phone,
                hashed_password=hashed_password,
                address=user.address,
                city=user.city,
                country=user.country,
                postal_code=user.postal_code,
                date_of_birth=user.date_of_birth,
                gender=user.gender,
                avatar_url=user.avatar_url,
                is_active=True,
            )
            db.add(db_user)
            await db.commit()
            await db.refresh(db_user)
            return db_user

        
    async def login(self, username: str, password: str, db: AsyncSession):
        result = await db.execute(
                          select(UserProfile)
                          .where(UserProfile.username == username)
                          )
        user = result.scalar_one_or_none()
        if not user:
            raise ServerException(
                status_code=HTTP_404_NOT_FOUND, detail="Unable to find this username"
            )
        matched = security.verify_password(password, user.hashed_password)
        if (matched):
              # create jwt token with configured TTL in MVP1
              # TODO: dynamically refresh token after each api call
            
            return {"access_token": create_access_token({"username": username}, timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)),
              "token_type": "bearer"}
        else:
            raise ServerException(status_code=HTTP_405_METHOD_NOT_ALLOWED, detail="Password doesn't match")
