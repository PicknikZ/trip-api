from fastapi import APIRouter, Depends, HTTPException
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession

from app.utils.errors.exceptions import ServerException
from app.utils.response.response import BaseResponse, CommonResponse
from .schemas import TripCreate, TripResponse
from app.services.trip import TripService
from app.database import get_db
from app.utils import get_logger
from app.dependencies import get_current_user

router = APIRouter()

@router.get("/trips/list", response_model=List[TripResponse])
async def list_trips(
    filter_type: Optional[str] = None,
    filter_value: Optional[str] = None,
    sort_by: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    logger= Depends(get_logger)
):
    logger.info("request trip list")
    try:
      return CommonResponse.success(data=await TripService.list_trips(db, filter_type, filter_value, sort_by))
    except ServerException as e:
      raise e
    except Exception as e:
        raise ServerException(
            status_code=500,
            detail=f"{e}"
        )

@router.post("/trips/create", response_model=TripResponse)
async def create_trip(trip_data: TripCreate, user = Depends(get_current_user), 
                      db: AsyncSession = Depends(get_db),
                      logger= Depends(get_logger)):
    logger.info(f"{user.username} request trip create")
    try:
      trip_data.owner_id = user.id
      logger.info(f"trip info {trip_data}")
      return CommonResponse.success(data=await TripService.create_trip(db, trip_data))
    except ServerException as e:
      raise e
    except Exception as e:
        raise ServerException(
            status_code=500,
            detail=f"{e}"
        )

@router.put("/trips/{trip_id}/pin")
async def pin_trip(trip_id: str, db: AsyncSession = Depends(get_db)):
    try:
      return CommonResponse.success(data=True, msg=await TripService.pin_trip(db, trip_id))
    except ServerException as e:
      raise e
    except Exception as e:
        raise ServerException(
            status_code=500,
            detail=f"{e}"
        )

@router.post("/trips/{trip_id}/favorite")
async def favorite_trip(trip_id: str, db: AsyncSession = Depends(get_db), user = Depends(get_current_user)):
    try:
      return CommonResponse.success(data=True, msg=await TripService.favorite_trip(db, trip_id, user))
    except ServerException as e:
      raise e
    except Exception as e:
        raise ServerException(
            status_code=500,
            detail=f"{e}"
        )

@router.post("/trips/{trip_id}/unfavorite")
async def unfavorite_trip(trip_id: str, db: AsyncSession = Depends(get_db), User = Depends(get_current_user)):
    try:
      return CommonResponse.success(data=True, msg=await TripService.unfavorite_trip(db, trip_id, User))
    except ServerException as e:
      raise e
    except Exception as e:
        raise ServerException(
            status_code=500,
            detail=f"{e}"
        )

@router.post("/trips/favorite", response_model=BaseResponse[List[TripResponse]])
async def favorite_trip(db: AsyncSession = Depends(get_db), User = Depends(get_current_user)):
    try:
      return CommonResponse.success(await TripService.my_favorite(db, User))
    except ServerException as e:
      raise e
    except Exception as e:
        raise ServerException(
            status_code=500,
            detail=f"{e}"
        )
    
    