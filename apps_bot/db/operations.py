from sqlalchemy import select 
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from db.tables.user import User

async def get_user(async_session: async_sessionmaker[AsyncSession],
                   telegram_id: int):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.telegram_id == telegram_id))       
        return result.scalar_one_or_none()


async def add_user(async_session: async_sessionmaker[AsyncSession],
                   telegram_id: int,
                   first_name: str,
                   last_name: str,
                   middle_name: str,
                   department: str):
    async with async_session() as session:
        async with session.begin():
                session.add(User(telegram_id=telegram_id,
                                 first_name=first_name,
                                 last_name=last_name,
                                 middle_name=middle_name,
                                 department=department))
                