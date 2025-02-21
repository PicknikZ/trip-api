from fastapi import APIRouter
from .user import router as user_router
from .trip import router as trip_router

router = APIRouter()

router.include_router(user_router)
router.include_router(trip_router)
