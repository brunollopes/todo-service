from datetime import datetime
import uuid

from pymongo import ReturnDocument
from ..config.database import Tasks
from ..model.todos_serializers import taskListEntity
from ..utils import util

log = util.getLog(__name__)
def count():
    return Tasks.count_documents({})
    
def find_tasks(pipeline):
    log.info("given: "+ str(pipeline))
    return taskListEntity(Tasks.aggregate(pipeline))

def find_tasks_by_boadId(boardId):
    log.info("given: "+ str(boardId))
    return Tasks.find({'board': boardId})

def find_task_by_taskId(taskId):
    log.info("given: "+ str(taskId))
    return Tasks.find_one({'id': taskId})

def find_tasks_by_userId(userId):
    log.info("given: "+ str(userId))
    return Tasks.find({'user': userId})
    
def create_task(payload):
    log.info("given: "+ str(payload))
    payload = prepare_task_payload(payload)
    
    try:
        result = Tasks.insert_one(payload.dict(exclude_none=False))
        return Tasks.find_one({'_id': result.inserted_id})
    except Exception as err:
        return str(err)
    

def replace_task(payload):
    log.info("given: "+ str(payload))
    payload = prepare_task_payload(payload)
    delete_task(payload.id)
    return create_task(payload)

def updated_task(payload, taskId):
    log.info("given payload: "+ str(payload) + " and taskId: "+ taskId)
    updated_task = Tasks.find_one_and_update(
        {'id': taskId}, {'$set': payload.dict(exclude_none=True)}, return_document=ReturnDocument.AFTER)
    return updated_task
   
def prepare_task_payload(payload):
    log.info("given payload: "+ str(payload))
    if payload.id == None:
        payload.id = str(uuid.uuid4())
    
    if payload.status == None: 
        payload.status = 'Created'
    
    payload.user = str(payload.user)
    payload.board = str(payload.board)
    payload.createdAt = datetime.utcnow()
    payload.updatedAt = payload.createdAt
    return payload


def drop_alltasks():
    Tasks.drop()


def delete_task(taskId: str):
    log.info("given: "+ str(taskId))
    return Tasks.find_one_and_delete({'id': taskId})

def delete_tasks_by_userId(userId: str):
    log.info("given: "+ str(userId))
    tasks = Tasks.find({'user': userId})
    for task in tasks:
        delete_task(task["id"])
    