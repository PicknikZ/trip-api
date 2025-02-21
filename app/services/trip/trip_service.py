from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional, List
from app.models import Trip, UserFavorite, UserProfile
from app.routers.v1.trip.schemas import TripCreate
from app.utils.errors.exceptions import ServerException
from app.utils.logging import logger

class TripService:
    @staticmethod
    async def list_trips(
        db: AsyncSession,
        filter_type: Optional[str] = None,
        filter_value: Optional[str] = None,
        sort_by: Optional[str] = None
    ) -> List[Trip]:
        """
        获取旅程列表，支持过滤和排序。
        
        :param db: 异步数据库会话
        :param filter_type: 过滤类型（如 "owner_id" 或 "is_pinned"）
        :param filter_value: 过滤值
        :param sort_by: 排序字段（如 "start_date" 或 "-start_date"）
        :return: 旅程列表
        """
        try:
            # 构建基础查询
            query = select(Trip)
            # 添加过滤条件
            if filter_type and filter_value:
                if filter_type == "owner_id":
                    query = query.where(Trip.owner_id == filter_value)
                elif filter_type == "is_pinned":
                    is_pinned = filter_value.lower() == "true" if isinstance(filter_value, str) else False
                    query = query.where(Trip.is_pinned == is_pinned)

            # 添加排序规则
            if sort_by:
                if sort_by == "start_date":
                    query = query.order_by(Trip.start_date.asc())
                elif sort_by == "-start_date":
                    query = query.order_by(Trip.start_date.desc())

            # 执行查询
            result = await db.execute(query)
            trips = result.scalars().all()

            # 记录日志
            logger.info(f"Retrieved {len(trips)} trips with filters: {filter_type}={filter_value}, sort_by={sort_by}")
            return trips

        except SQLAlchemyError as e:
            # 捕获数据库相关异常
            logger.error(f"Database error while listing trips: {e}")
            raise ServerException(status_code=500, detail="Database error")
        except ServerException as e:
            await db.rollback()
            raise e
        except Exception as e:
            # 捕获其他异常
            logger.error(f"Unexpected error while listing trips: {e}")
            raise ServerException(status_code=500, detail="Internal server error")

    @staticmethod
    async def create_trip(db: AsyncSession, trip_data: TripCreate):
        """
        创建新旅程。
        
        :param db: 异步数据库会话
        :param trip_data: 旅程创建数据
        :return: 新创建的旅程对象
        """
        try:
            # 验证输入数据
            new_trip = Trip(**trip_data.dict())
            
            # 插入数据
            db.add(new_trip)
            await db.commit()
            await db.refresh(new_trip)
            
            logger.info(f"Created new trip with ID: {new_trip.id}")
            return new_trip

        except SQLAlchemyError as e:
            logger.error(f"Database error while creating trip: {e}")
            await db.rollback()
            raise ServerException(status_code=500, detail="Database error")
        except ServerException as e:
            await db.rollback()
            raise e
        except Exception as e:
            logger.error(f"Unexpected error while creating trip: {e}")
            await db.rollback()
            raise ServerException(status_code=500, detail="Internal server error")

    @staticmethod
    async def pin_trip(db: AsyncSession, trip_id: str):
        """
        置顶指定旅程。
        
        :param db: 异步数据库会话
        :param trip_id: 旅程 ID
        :return: 成功消息
        """
        try:
            # 查询旅程
            query = select(Trip).where(Trip.id == trip_id)
            result = await db.execute(query)
            trip = result.scalar_one_or_none()

            if not trip:
                logger.warning(f"Trip with ID {trip_id} not found")
                raise ServerException(status_code=404, detail="Trip not found")

            # 更新置顶状态
            trip.is_pinned = True
            await db.commit()

            logger.info(f"Pinned trip with ID: {trip_id}")
            return {"message": "Trip pinned successfully"}

        except SQLAlchemyError as e:
            logger.error(f"Database error while pinning trip: {e}")
            await db.rollback()
            raise ServerException(status_code=500, detail="Database error")
        except ServerException as e:
            await db.rollback()
            raise e
        except Exception as e:
            logger.error(f"Unexpected error while pinning trip: {e}")
            await db.rollback()
            raise ServerException(status_code=500, detail="Internal server error")

    @staticmethod
    async def favorite_trip(db: AsyncSession, trip_id: str, current_user: UserProfile):
        """
        收藏指定旅程。
        
        :param db: 异步数据库会话
        :param trip_id: 旅程 ID
        :param current_user: 当前用户
        :return: 成功消息
        """
        try:
            # 查询旅程
            query = select(Trip).where(Trip.id == trip_id)
            result = await db.execute(query)
            trip = result.scalar_one_or_none()

            if not trip:
                raise ServerException(status_code=404, detail="Trip not found")

            # 检查是否已收藏
            query = select(UserFavorite).where(
                UserFavorite.user_id == current_user.id,
                UserFavorite.trip_id == trip_id
            )
            result = await db.execute(query)
            existing_favorite = result.scalar_one_or_none()

            if existing_favorite:
                raise ServerException(status_code=400, detail="Trip already favorited")

            # 创建收藏记录
            favorite = UserFavorite(user_id=current_user.id, trip_id=trip_id)
            db.add(favorite)
            await db.commit()

            logger.info(f"User {current_user.id} favorited trip {trip_id}")
            return "Trip favorited successfully"

        except SQLAlchemyError as e:
            logger.error(f"Database error while favoriting trip: {e}")
            await db.rollback()
            raise ServerException(status_code=500, detail="Database error")
        except ServerException as e:
            await db.rollback()
            raise e
        except Exception as e:
            logger.error(f"Unexpected error while favoriting trip: {e}")
            await db.rollback()
            raise ServerException(status_code=500, detail="Internal server error")

    @staticmethod
    async def unfavorite_trip(db: AsyncSession, trip_id: str, current_user: UserProfile):
        """
        取消收藏指定旅程。
        
        :param db: 异步数据库会话
        :param trip_id: 旅程 ID
        :param current_user: 当前用户
        :return: 成功消息
        """
        try:
            # 查询旅程
            query = select(Trip).where(Trip.id == trip_id)
            result = await db.execute(query)
            trip = result.scalar_one_or_none()

            if not trip:
                raise ServerException(status_code=404, detail="Trip not found")

            # 检查是否已收藏
            query = select(UserFavorite).where(
                UserFavorite.user_id == current_user.id,
                UserFavorite.trip_id == trip_id
            )
            result = await db.execute(query)
            favorite = result.scalar_one_or_none()

            if not favorite:
                raise ServerException(status_code=400, detail="Trip not favorited")

            # 删除收藏记录
            await db.delete(favorite)
            await db.commit()

            logger.info(f"User {current_user.id} unfavorited trip {trip_id}")
            return "Trip unfavorited successfully"

        except SQLAlchemyError as e:
            logger.error(f"Database error while unfavoriting trip: {e}")
            await db.rollback()
            raise ServerException(status_code=500, detail="Database error")
        except ServerException as e:
            await db.rollback()
            raise e
        except Exception as e:
            logger.error(f"Unexpected error while unfavoriting trip: {e}")
            await db.rollback()
            raise ServerException(status_code=500, detail="Internal server error")
    
    @staticmethod   
    async def my_favorite(db: AsyncSession, current_user: UserProfile) -> List[Trip]:
        """
        获取当前用户的收藏旅程列表。
        
        :param db: 数据库会话
        :param current_user: 当前用户对象
        :return: 用户收藏的旅程列表
        """
        try:
            # 使用 JOIN 查询直接获取用户收藏的旅程
            query = (
                select(Trip)
                .join(UserFavorite, Trip.id == UserFavorite.trip_id)
                .where(UserFavorite.user_id == current_user.id)
            )
            
            # 执行查询
            result = await db.execute(query)
            my_favorite_trips = result.scalars().all()

            # 如果没有收藏记录，返回空列表
            if not my_favorite_trips:
                logger.info(f"User {current_user.username} has no favorite trips.")
                return []

            logger.info(
                f"Retrieved {len(my_favorite_trips)} favorite trips for user {current_user.username}."
            )
            return my_favorite_trips

        except SQLAlchemyError as e:
            # 捕获数据库相关异常
            logger.error(
                f"Database error while querying favorite trips for user {current_user.username}: {e}"
            )
            raise ServerException(status_code=500, detail="Database error")
        except ServerException as e:
            await db.rollback()
            raise e
        except Exception as e:
            # 捕获其他异常
            logger.error(
                f"Unexpected error while querying favorite trips for user {current_user.username}: {e}"
            )
            raise ServerException(status_code=500, detail="Internal server error")