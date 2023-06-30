import logging
import asyncio

from aiogram import Dispatcher, Bot

from sqlalchemy.ext.asyncio import async_sessionmaker
from redis.asyncio import Redis

from config import bot_config

from handlers.registration import reg_router
from handlers.send_question import question_router

from db.setup import proceed_schemas
from db.setup import create_engine


async def main():
    redis = Redis(db=3)
    dp = Dispatcher()
    bot = Bot(bot_config.bot_token)
    dp.include_routers(reg_router, question_router)
    
    engine = create_engine()
    async_session = async_sessionmaker(engine)
    await proceed_schemas(engine)
    
 
    await dp.start_polling(bot,
                           async_session=async_session,
                           redis=redis)
                
 
    await engine.dispose()
    

def cli():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s [%(levelname)s]: %(message)s',
                        datefmt='%Y/%m/%d %H:%M.%S')
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.error('Bot stopped.')


if __name__ == '__main__':
    cli()
    