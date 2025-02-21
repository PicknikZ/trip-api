from sqlalchemy import Column, CHAR, VARCHAR, DATE, Integer, JSON, SmallInteger, DATETIME, Index, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
from uuid import uuid4


class Trip(Base):
    __tablename__ = 'trips'

    # 主键
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # 外键：创建者ID
    owner_id = Column(CHAR(36), ForeignKey('users.id'))
    
    # 其他字段
    title = Column(VARCHAR(100), nullable=False)
    start_date = Column(DATE, nullable=False)
    duration = Column(Integer, nullable=False)
    cities = Column(JSON, nullable=False)
    style_tags = Column(JSON, nullable=False)
    settings = Column(JSON, nullable=False)
    is_pinned = Column(SmallInteger, default=0)
    
    # 时间戳
    created_at = Column(DATETIME, default=func.now())
    # 关系映射
    favorited_by = relationship("UserFavorite", back_populates="trip")


class TripMember(Base):
    __tablename__ = 'trip_members'

    # 联合主键
    trip_id = Column(Integer, ForeignKey('trips.id'), primary_key=True)
    user_id = Column(CHAR(36), ForeignKey('users.id'), primary_key=True)

    # 其他字段
    role = Column(SmallInteger, default=1)  # 默认值为 1（成员）
    joined_at = Column(DATETIME, default=func.now())




class UserFavorite(Base):
    __tablename__ = 'user_favorites'

    # 联合主键
    user_id = Column(CHAR(36), ForeignKey('users.id'), primary_key=True, nullable=False)
    trip_id = Column(Integer, ForeignKey('trips.id'), primary_key=True, nullable=False)

    # 时间戳
    created_at = Column(DATETIME, server_default=func.now())

    # 关系映射
    user = relationship("UserProfile", back_populates="favorites")
    trip = relationship("Trip", back_populates="favorited_by")