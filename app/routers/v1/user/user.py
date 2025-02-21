from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import UserProfile
from app.utils.errors.exceptions import ServerException
from .schemas import UserCreate, UserLogin, UserResponse, Token
from app.database import get_db
from app.services.user import User
from app.dependencies import get_current_user
from app.utils import get_logger

router = APIRouter()

@router.post("/user/register", response_model=UserResponse)
async def register_user(User_profile: UserCreate, db: AsyncSession = Depends(get_db), 
                  logger= Depends(get_logger)):
    logger.info(f"register user request received for user: {User_profile.username}")
    user = User()
    try:
      return await user.register_user(User_profile, db)
    except ServerException as e:
       raise e
    except Exception as e:
        raise ServerException(
            status_code=500,
            detail=f"{e}"
        )

@router.post("/user/login", response_model=Token)
async def login_for_access_token(form_data: UserLogin, db: AsyncSession = Depends(get_db),
                           logger= Depends(get_logger)):
    logger.info(f"login user request received for user: {form_data.username}")
    user = User()
    try:
       return await user.login(form_data.username, form_data.password, db)
    except ServerException as e:
       raise e
    except Exception as e:
        raise ServerException(
            status_code=500,
            detail=f"{e}"
        )

@router.get("/users/me", response_model=UserResponse)
def read_users_me(current_user: UserProfile = Depends(get_current_user)):
    return current_user