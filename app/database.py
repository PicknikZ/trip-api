from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.pool import NullPool 
from sqlalchemy import text
from app.config import settings

# 异步引擎配置（注意驱动改为 asyncmy）
# 格式：mysql+asyncmy://user:password@host:port/database
engine = create_async_engine(
    settings.DATABASE_URL,  # 替换驱动标识
    echo=True,                      # 开发时显示SQL日志
    poolclass=NullPool,
    # pool_size=20,                   # 连接池大小
    # max_overflow=50,                # 最大溢出连接数
    # pool_recycle=3600,              # 连接回收时间
    # pool_pre_ping=True,             # 连接活性检查
    connect_args={
        "charset": "utf8mb4"        # 字符集配置
    }
)

# 异步会话工厂
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,            # 明确指定异步会话类
    autocommit=False,
    autoflush=False,
    expire_on_commit=False          # 避免属性过期问题
)

Base = declarative_base()

async def init_db():
    async with engine.begin() as conn:
        # 检查连接
        await conn.execute(text("SELECT 1"))
        print("✅ Database connection successful")
        
        # 创建所有表（需确保数据库已存在）
        await conn.run_sync(Base.metadata.create_all)
        print("✅ Tables created")

async def get_db() -> AsyncSession: # type: ignore
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()  # 自动提交事务（可选）
        except Exception as e:
            await session.rollback()  # 自动回滚
            raise e
        finally:
            await session.close()