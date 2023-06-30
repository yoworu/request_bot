from typing import Callable, Awaitable, Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from redis.asyncio import Redis
from db.operations import get_user


class CheckRegistration(BaseMiddleware):
    async def __call__(self,
                       handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
                       event: TelegramObject,
                       data: dict[str, Any]) -> Any:
        
        redis: Redis = data['redis']
        async_session = data['async_session']
        
        user_in_redis = await redis.get(event.from_user.id)

        if user_in_redis:
            return await handler(event, data)
        else:
            user = await get_user(async_session, event.from_user.id)

            if user:        
                await redis.set(event.from_user.id, event.from_user.id)
                return await handler(event, data)
            else:
                await event.answer('/registration')
            