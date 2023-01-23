import json
import unittest
from uuid import UUID

import requests
from app.tests import testutilities
from app.controller import board
from ..app import app
import vcr
import sys
from fastapi.testclient import TestClient

PRINT = True            # change to False when finished debugging...

client = TestClient(app) 

    
class TestTaskValidator (unittest.TestCase):
    
    @classmethod
    def setUpClass( JsonValidateTest ):
        testutilities.turnOnPrinting( PRINT )
        
    
    def setUp( self ):
        pass
        TEST_VALID_BOARD_JSON = {
                "name": "t1"
        }
        res = client.post("/api/boards/",json=TEST_VALID_BOARD_JSON)
        self.boardId = res.json()["board"]["id"]
        TEST_VALID_TASK_JSON = {
            "name": "t1",
            "user": "9f97dd87-ac90-4b88-a378-749b130e34d4",
            "board": self.boardId
        }
        res =  client.post("/api/tasks/",json=TEST_VALID_TASK_JSON)
        self.taskId = res.json()["task"]["id"]
        
    def tearDown( self ):
        pass
        client.delete("/api/boards/"+self.boardId) #delete all boards and tasks

    def test_GetAllTasksByBoardId(self):
        testutilities.printTestCaseName( sys._getframe().f_code.co_name )
        boardId = self.boardId
        
        response = client.get("/api/tasks?page=1&limit=10&search="+boardId)
        
        assert response.json()["results"] == 1
    
    def test_GivenAValidTaskJsonReturn201(self):
        testutilities.printTestCaseName( sys._getframe().f_code.co_name )
        NEW_JSON = {
            "name": "t3",
            "user": "9f97dd87-ac90-4b88-a378-749b130e34d4",
            "board": self.boardId
        }
        response = client.post("/api/tasks/",json=NEW_JSON)
        assert response.status_code == 201
        assert response.json()["task"]["name"] == NEW_JSON["name"]
        assert response.json()["task"]["board"] == NEW_JSON["board"]
        
    def test_GivenAInValidTaskJsonReturn422(self):
        testutilities.printTestCaseName( sys._getframe().f_code.co_name )
                
        TEST_INVALID_JSON = {
                    "name": "t1",
                    "code": "123"
                }
        response = client.post("/api/tasks/",json=TEST_INVALID_JSON)
        assert response.status_code == 422
    
    def test_GivenAInValidTaskJsonExpectReplacement200(self):
        testutilities.printTestCaseName( sys._getframe().f_code.co_name )
                
        res = client.get("/api/tasks/"+self.taskId)
        assert res.status_code == 200
        assert res.json()["task"]["name"] == "t1"
        
        NEW_TASK_JSON = {
            "name": "t11",
            "description": "desc11",
            "status": "Started",
            "user": "9f97dd87-ac90-4b88-a378-749b130e34d4",
            "board": self.boardId
        }
        
        response = client.put("/api/tasks/"+self.taskId,json=NEW_TASK_JSON)
        assert response.status_code == 200
        assert response.json()["task"]["id"] == self.taskId
        assert response.json()["task"]["name"] == NEW_TASK_JSON["name"]
        
        response = client.get("api/tasks/")
        assert response.status_code == 200
        assert response.json()["results"] == 1
        
     
    def test_GivenAInValidTaskJsonExpectUpdate200(self):
        testutilities.printTestCaseName( sys._getframe().f_code.co_name )
                
        res = client.get("/api/tasks/"+self.taskId)
        assert res.status_code == 200
        assert res.json()["task"]["name"] == "t1"
        
        NEW_TASK_JSON = {
            "name": "t11 update",
            "description": "desc11 update",
            "status": "Completed"
        }
        
        response = client.patch("/api/tasks/"+self.taskId,json=NEW_TASK_JSON)
        assert response.status_code == 200
        assert response.json()["task"]["id"] == self.taskId
        assert response.json()["task"]["name"] == NEW_TASK_JSON["name"]
        assert response.json()["task"]["description"] == NEW_TASK_JSON["description"]
        assert response.json()["task"]["status"] == NEW_TASK_JSON["status"]
        
        response = client.get("api/tasks/")
        assert response.status_code == 200
        assert response.json()["results"] == 1
        
    def test_GivenTaskIdExpectDeletionReturn204(self):
        testutilities.printTestCaseName( sys._getframe().f_code.co_name )
        
        NEW_JSON = {
                "name": "t3",
                "user": "9f97dd87-ac90-4b88-a378-749b130e34d4",
                "board": self.boardId
            }
        
        res = client.post("/api/tasks/",json=NEW_JSON)
        
        response = client.get("api/tasks/")
        assert response.status_code == 200
        assert response.json()["results"] == 2
 
        taskId = res.json()["task"]["id"]
        response = client.delete("/api/tasks/"+taskId)
        assert response.status_code == 204
        
        response = client.get("api/tasks/")
        assert response.status_code == 200
        assert response.json()["results"] == 1
    
    def test_GivenAUserDeletionValidJsonDeletesAllTasksReturn204(self):
        testutilities.printTestCaseName( sys._getframe().f_code.co_name )
        
        NEW_JSON = {
                "name": "t3",
                "user": "9f97dd87-ac90-4b88-a378-749b130e34d4",
                "board": self.boardId
            }
        
        res = client.post("/api/tasks/",json=NEW_JSON)
        
        response = client.get("api/tasks/users/"+NEW_JSON["user"])
        assert response.status_code == 200
        assert response.json()["results"] == 2
        
        USER_DELETED_JSON = {
            "time": "2021-07-06T14:48:00.000Z",
            "data": {
                "user": "9f97dd87-ac90-4b88-a378-749b130e34d4"
            }   
        }
        
        res = client.post("/api/webhooks/user-deleted/",json=USER_DELETED_JSON)
        assert res.status_code == 204
        
        response = client.get("api/tasks/users/"+NEW_JSON["user"])
        assert response.status_code == 200
        assert response.json()["results"] == 0
        
        

if __name__ == '__main__':
    unittest.main()