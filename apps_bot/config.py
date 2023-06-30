import configparser
from dataclasses import dataclass

parser = configparser.ConfigParser()
parser.read('bot.ini')



@dataclass
class DbConfig:
    host: str
    port: int
    user: str
    password: str
    database: str 
    

@dataclass
class BotConfig:
    bot_token: str
    channel_id: int
    

HOST = parser.get('PostgresDB', 'host')
PORT = parser.getint('PostgresDB', 'port')
USER = parser.get('PostgresDB', 'user')
PASSWORD = parser.get('PostgresDB', 'password')
DATABASE = parser.get('PostgresDB', 'database')

BOT_TOKEN = parser.get('TelegramBot', 'Token')
CHANNEL_ID = parser.get('TelegramBot', 'channel_id')

db_config = DbConfig(HOST, PORT, USER, PASSWORD, DATABASE)
db_uri =(
    f'postgresql+asyncpg://{db_config.user}:{db_config.password}@{db_config.host}:{db_config.port}/{db_config.database}'
)
bot_config = BotConfig(BOT_TOKEN, CHANNEL_ID)

