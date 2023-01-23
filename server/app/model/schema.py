from datetime import datetime
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, constr
from bson.objectid import ObjectId

from app.model.schemaGen import Task, BoardSchema
        
class TaskBaseSchema(Task):
    createdAt: datetime | None = None
    updatedAt: datetime | None = None
    board: Optional[UUID] = None
    userData: Optional[dict] = dict('')
    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str} 


class BoardBaseSchema(BoardSchema):
    createdAt: datetime | None = None
    updatedAt: datetime | None = None
    tasks: Optional[List[TaskBaseSchema]] = []
    
    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        
class UpdateBoardSchema(BoardSchema):
    name: str | None = None
    description: str | None = None
   
    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        
class UpdateTaskSchema(Task):
    name: str | None = None
    user: UUID | None = None
    description: str | None = None
    status: str | None = None
    board: UUID | None = None
    updatedAt: datetime | None = None
    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class UserDeletedSchema(BaseModel):
    createdAt: datetime | None = None
    updatedAt: datetime | None = None
    tasks: Optional[List[TaskBaseSchema]] = []
    
    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        
class BoardResponse(BaseModel):
    status: str
    board: BoardBaseSchema

class TaskResponse(BaseModel):
    status: str
    task: TaskBaseSchema

class ListBoardResponse(BaseModel):
    status: str
    results: int
    boards: List[BoardBaseSchema]

class ListTaskResponse(BaseModel):
    status: str
    results: int
    tasks: List[TaskBaseSchema]

class CountBoardResponse(BaseModel):
    status: str
    results: int

class CountTaskResponse(BaseModel):
    status: str
    results: int
