from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from config import DB_URI

engine = create_async_engine(DB_URI, echo=False)

# async_sessionmaker — более современный вариант вместо sessionmaker
AsyncSessionFactory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)