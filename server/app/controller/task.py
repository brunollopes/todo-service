from fastapi import HTTPException, status, APIRouter, Response
from app.model import schema
from app.config.database import Tasks
from app.model.todos_serializers import taskEntity, taskListEntity
from ..utils import util
from ..service import taskService
from ..utils import util

log = util.getLog(__name__)

router = APIRouter() 


@router.get('/count', response_model=schema.CountTaskResponse)
def count_tasks():
    log.info("call to GET api/tasks/count")
    return {'status': 'success', 'results': taskService.count()}


@router.get('/', response_model=schema.ListTaskResponse)
def get_tasks_by_boardId(limit: int = 10, page: int = 1, search: str = ''):
    log.info("call to GET api/tasks/")
    skip = (page - 1) * limit
    pipeline = [
        {'$match': {'board': {'$regex': search, '$options': 'i'}}},
        {
            '$skip': skip
        }, {
            '$limit': limit
        }
    ]
    tasks = taskService.find_tasks(pipeline)
    return {'status': 'success', 'results': len(tasks), 'page': page, 'tasks': tasks}


@router.get('/{taskId}', response_model=schema.TaskResponse)
def get_task_by_taskId(taskId: str):
    log.info("call to GET api/tasks/{taskId}}")
    if not util.validate_uuidv4(taskId):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Invalid id: {taskId}")

    task = taskService.find_task_by_taskId(taskId)
    
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No board with this id: {taskId} found")
    
    return {"status": "success", "task": taskEntity(task)}



@router.get('/users/{userId}', response_model=schema.ListTaskResponse)
def get_tasks_by_userId(userId: str):
    log.info("call to GET api/tasks/users/{userId}")
    if not util.validate_uuidv4(userId):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Invalid id: {userId}")

    tasks = taskService.find_tasks_by_userId(userId)
    
    tasksList = list()
    for task in tasks:
        tasksList.append(task);
        
    if not tasks:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No tasks for user with this id: {userId} found")
    
    return {"status": "success", "results":len(tasksList), "tasks": taskListEntity(tasksList)}

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schema.TaskResponse)
def create_task(payload: schema.TaskBaseSchema):
    log.info("call to POST api/tasks/")
    res = taskService.create_task(payload)
    if res == None or type(res) == str or not res["name"] == payload.name:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                        detail=res)
    return {"status": "success", "task": taskEntity(res)}
 

@router.patch('/{taskId}', response_model=schema.TaskResponse)
def update_task(taskId: str, payload: schema.UpdateTaskSchema):
    log.info("call to PATCH api/tasks/{taskId}")
    if not util.validate_uuidv4(taskId):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Invalid id: {taskId}")
        
    updated_task = taskService.updated_task(payload,taskId)
    
    if not updated_task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No task with this id: {taskId} found')
    return {"status": "success", "task": taskEntity(updated_task)}


    
@router.put('/{taskId}', response_model=schema.TaskResponse)
def replace_task(taskId: str, payload: schema.TaskBaseSchema):
    log.info("call to PUT api/tasks/{taskId}")
    if not util.validate_uuidv4(taskId):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Invalid id: {taskId}")
    payload.id = taskId
    
    replaced_task = taskService.replace_task(payload)    
   
    if not replaced_task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No task with this id: {taskId} found')
    return {"status": "success", "task": taskEntity(replaced_task)}


@router.delete('/')
def delete_alltasks():
    log.info("call to DELETE api/tasks/")
    taskService.drop_alltasks()
    return Response(status_code=status.HTTP_200_OK)


@router.delete('/{taskId}')
def delete_task(taskId: str):
    log.info("call to DELETE api/tasks/{taskId}")
    if not util.validate_uuidv4(taskId):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Invalid id: {taskId}")
    
    task = taskService.delete_task(taskId)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No task with this id: {taskId} found')
    return Response(status_code=status.HTTP_204_NO_CONTENT)
