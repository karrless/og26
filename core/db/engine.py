from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from config import DB_URI

engine = create_async_engine(DB_URI, echo=False)

AsyncSessionFactory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)