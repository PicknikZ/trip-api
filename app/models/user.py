from uuid import uuid4
from sqlalchemy import Column, Index, Integer, String, Boolean, DateTime, Enum, text, CHAR
from sqlalchemy.dialects.mysql import ENUM as MySQLENUM
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class UserProfile(Base):
    __tablename__ = "users"
    __table_args__ = {
        'mysql_engine': 'InnoDB',          # 指定存储引擎
        'mysql_charset': 'utf8mb4',        # 设置字符集
        'mysql_collate': 'utf8mb4_unicode_ci'  # 设置校对规则
    }

    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid4().hex))
    username = Column(String(255), unique=True, nullable=False, index=True)  # 限定用户名长度
    full_name = Column(String(100), index=True)               # 优化姓名长度
    phone = Column(String(20), nullable=True)                 # 包含国家代码的格式
    hashed_password = Column(String(255), nullable=False)     # 适配bcrypt等哈希长度
    address = Column(String(255), nullable=True)
    city = Column(String(50), nullable=True)
    country = Column(String(20), nullable=True)                # ISO国家码标准
    postal_code = Column(String(20), nullable=True)
    date_of_birth = Column(DateTime, nullable=True)
    gender = Column(
        MySQLENUM('male', 'female', 'other', 'undisclosed', name='gender_enum'),
        nullable=True,
        server_default='undisclosed'
    )  # 使用MySQL原生ENUM类型
    avatar_url = Column(String(512), nullable=True)           # 适配长URL
    is_active = Column(Boolean, server_default=text("TRUE"))   # 默认值写服务端
    created_at = Column(
        DateTime,
        server_default=text('CURRENT_TIMESTAMP'),  # 使用MySQL的时间函数
        nullable=False
    )
    updated_at = Column(
        DateTime, 
        server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'),
        nullable=False
    )  # 自动更新时间戳

    # 关系映射
    favorites = relationship("UserFavorite", back_populates="user")

    # 添加复合索引（按业务需求）
    __table_args__ = (
        Index('idx_city_country', 'city', 'country'),
    )
