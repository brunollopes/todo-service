
from fastapi import APIRouter, HTTPException, status
from ..utils import util
from ..service import taskService
from ..model import userDeletedSchemaGen
from ..utils import util

log = util.getLog(__name__)

router = APIRouter() 

@router.post("/user-deleted",status_code=status.HTTP_204_NO_CONTENT)
def user_deleted(payload: userDeletedSchemaGen.UserDeleted):
    log.info("call to POST api/webhooks/user-deleted")
    if not util.validate_uuidv4(payload.data.user):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Invalid id: {payload.data.user}")
    try:
        taskService.delete_tasks_by_userId(payload.data.user)
        return None    
    except Exception as err:
        return str(err)