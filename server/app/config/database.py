from pymongo import mongo_client, ASCENDING
from app.config.config import settings
from ..utils import util

log = util.getLog(__name__)

client = mongo_client.MongoClient(settings.DATABASE_URL)
print('🚀 Connected to MongoDB...')
log.info("🚀 Connected to MongoDB...")

db = client[settings.MONGO_INITDB_DATABASE]
Boards = db.boards
Boards.create_index([("name", ASCENDING)], unique=True)
Boards.create_index([("id", ASCENDING)], unique=True)
Tasks = db.tasks
Tasks.create_index([("name", ASCENDING)], unique=True)
Tasks.create_index([("id", ASCENDING)], unique=True)
log.info("MongoDB collections index created.")

