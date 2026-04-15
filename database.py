from sqlalchemy import AsyncAdaptedQueuePool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./my_db.sqlite3"

connect_args = {"check_same_thread": False} if SQLALCHEMY_DATABASE_URL.startswith("sqlite") else {}

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=False, future=True, connect_args=connect_args)

AsyncSessionLocal = async_sessionmaker(bind=engine, 
                                       autoflush=False, 
                                       expire_on_commit=False,
                                       autocommit=False, 
                                       future=True,
                                       class_=AsyncSession)

class Base(DeclarativeBase):
    pass

async def get_db():
    async with AsyncSessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()
        
    
async def init_db():
    import user, message, chat
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)