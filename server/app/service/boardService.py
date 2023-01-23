from datetime import datetime
import uuid
from ..config.database import Boards
from ..model.todos_serializers import boardListEntity
from ..utils import util

log = util.getLog(__name__)

def count():
    log.info("count number of boards")
    return Boards.count_documents({})
    
def find_boards(pipeline):
    log.info("given: "+ str(pipeline))
    return boardListEntity(Boards.aggregate(pipeline))

def find_board_by_boadId(boardId):
    log.info("given: "+ str(boardId))
    return Boards.find_one({'id': boardId})
    
def create_board(payload):
    log.info("given: "+ str(payload))
    payload.id = str(uuid.uuid4())
    payload.createdAt = datetime.utcnow()
    payload.updatedAt = payload.createdAt
    try:
        result = Boards.insert_one(payload.dict(exclude_none=True))
        return Boards.find_one({'_id': result.inserted_id})
    except Exception as err:
        return str(err)

def drop_allboards():
    Boards.drop()


def delete_board(boardId: str):
    log.info("given: "+ boardId)
    return Boards.find_one_and_delete({'id': boardId})
    