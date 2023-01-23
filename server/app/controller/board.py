
from fastapi import HTTPException, status, APIRouter, Response

from ..service import userService
from ..model import schema
from ..config.database import Boards, Tasks
from ..model.todos_serializers import boardEntity, boardListEntity, taskEntity, taskListEntity
from ..utils import util
from ..service import taskService, boardService
from ..utils import util

log = util.getLog(__name__)

router = APIRouter() 


@router.get('/count', response_model=schema.CountBoardResponse)
def count_board():
    log.info("call to GET api/boards/count")
    return {'status': 'success', 'results': boardService.count()}


@router.get('/', response_model=schema.ListBoardResponse)
def get_boards(limit: int = 10, page: int = 1, search: str = ''):
    log.info("call to GET api/boards/")
    skip = (page - 1) * limit
    pipeline = [
        {'$match': {'id': {'$regex': search, '$options': 'i'}}},
        {
            '$skip': skip
        }, {
            '$limit': limit
        }
    ]
    boards = boardService.find_boards(pipeline)
    return {'status': 'success', 'results': len(boards), 'page': page, 'boards': boards}


@router.post('/{boardId}/tasks', status_code=status.HTTP_201_CREATED, response_model=schema.TaskResponse)
def create_board(boardId: str, payload: schema.TaskBaseSchema):
    log.info("call to POST api/boards/{boardId}/tasks")
    payload.board = boardId
    res = taskService.create_task(payload)
    if not res["name"] == payload.name:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                        detail=res)
    return {"status": "success", "task": taskEntity(res)}


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schema.BoardResponse)
def create_board(payload: schema.BoardBaseSchema):
    log.info("call to POST api/boards/")
    res = boardService.create_board(payload)
    if res == None or type(res) == str or not res["name"] == payload.name:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                        detail=res)
    return {"status": "success", "board": boardEntity(res)}

@router.get('/{boardId}', response_model=schema.BoardResponse)
def get_board(boardId: str):
    log.info("call to GET api/boards/{boardId}")
    if not util.validate_uuidv4(boardId):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Invalid id: {boardId}")

    board = boardService.find_board_by_boadId(boardId)
    
    if not board:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No board with this id: {boardId} found")
    
    tasks= taskService.find_tasks_by_boadId(boardId)
    tasksList = list()
    #enrich tasks with userdata
    for task in tasks:
        userUUId = task["user"]
        userData = userService.get_user_by_uuid(userUUId)
        task["userData"] = userData
        tasksList.append(task)
    
    boardDTO = boardEntity(board)
    boardDTO["tasks"] = taskListEntity(tasksList)
    
    return {"status": "success", "board": boardDTO}


@router.delete('/{boardId}')
def delete_board(boardId: str):
    log.info("call to DELETE api/boards/{boardId}")
    if not util.validate_uuidv4(boardId):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Invalid id: {boardId}")
        
    tasks = taskService.find_tasks_by_boadId(boardId)
    
    for task in tasks:
        taskService.delete_task(task["id"])
    
    board = boardService.delete_board(boardId)
    
    if not board:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No board with this id: {boardId} found')
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.delete('/')
def delete_allboards():
    log.info("call to DELETE api/boards/")
    boardService.drop_allboards()
    return Response(status_code=status.HTTP_200_OK)
