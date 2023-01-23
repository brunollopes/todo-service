from pydantic import BaseSettings
from ..utils import util

log = util.getLog(__name__)

class Settings(BaseSettings):
    log.info("Mongodb settings")
    DATABASE_URL: str = 'mongodb://todosdbuser:password123@mongo:27017/todosdb?authSource=admin'
    MONGO_INITDB_DATABASE: str = 'todosdb'

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
