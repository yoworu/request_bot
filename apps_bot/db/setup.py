
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from db.tables.base import Base

from config import db_uri

def create_engine():
    return create_async_engine(db_uri) 


async def proceed_schemas(engine: AsyncEngine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        

