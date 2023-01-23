
import unittest

from ..service import userService
from ..tests import testutilities
from ..app import app
import sys
from fastapi.testclient import TestClient

PRINT = True            # change to False when finished debugging...

client = TestClient(app) 

    
class TestBoardValidator (unittest.TestCase):
    
    @classmethod
    def setUpClass( JsonValidateTest ):
        testutilities.turnOnPrinting( PRINT )
        
    
    def setUp( self ):
        TEST_VALID_JSON = {
            "name": "t1"
        }
        res = client.post("/api/boards/",json=TEST_VALID_JSON)
        try:
            self.boardId = res.json()["board"]["id"]
        except KeyError:
            print(res.json()["detail"])
        
    def tearDown( self ):
        client.delete("/api/boards/"+self.boardId)

    def test_isAliveReturn200(self):
        testutilities.printTestCaseName( sys._getframe().f_code.co_name )
        response = client.get("/")
        assert response.status_code == 200
        assert response.json()["message"] == str("server is alive!")
    
    def test_GetBoardByBoardIdAndPaginationReturn200(self):
        testutilities.printTestCaseName( sys._getframe().f_code.co_name )
        
        response = client.get("/api/boards?page=1&limit=10&search="+self.boardId)
        assert response.status_code == 200
        assert response.json()["results"] == 1
    
    def test_GetBoardByBoardIdWithTasksAndUserData200(self):
        testutilities.printTestCaseName( sys._getframe().f_code.co_name )
        
        # add two tasks to the existing board
        user = userService.get_randomUser()
        userUID  = user["login"]["uuid"]
        
        client.post("/api/boards/"+self.boardId+"/tasks",json={
            "name": "Task name #1",
            "user": userUID,
            "board": self.boardId
        })
        
        client.post("/api/boards/"+self.boardId+"/tasks",json={
            "name": "Task name #2",
            "user": userUID,
            "board": self.boardId
        })
        
        response = client.get("/api/boards/"+self.boardId)
        assert response.status_code == 200
        
        board = response.json()["board"]
        tasks = board["tasks"]
        assert len(tasks) == 2
        
        for task in tasks:
            userdata = task["userData"] 
            assert not userdata == None
            
        
    def test_GivenAValidBoardJsonReturn201(self):
        testutilities.printTestCaseName( sys._getframe().f_code.co_name )
        NEW_JSON = {
            "name": "t2"
        }
        response = client.post("/api/boards/",json=NEW_JSON)
        assert response.status_code == 201
        assert response.json()["board"]["name"] == NEW_JSON["name"]
        
        
        boardId = response.json()["board"]["id"]
        client.delete("/api/boards/"+boardId)
        
        
    def test_GivenAValidTaskJsonAddItToExistingBoardReturn201(self):
        testutilities.printTestCaseName( sys._getframe().f_code.co_name )
        NEW_TASK_JSON = {
            "name": "t1",
            "user": "9f97dd87-ac90-4b88-a378-749b130e34d4"
        }
        response = client.post("/api/boards/"+self.boardId+"/tasks",json=NEW_TASK_JSON)
        assert response.status_code == 201
        assert response.json()["task"]["name"] == NEW_TASK_JSON["name"]
        
        
    def test_GivenAInValidBoardJsonReturn422(self):
        testutilities.printTestCaseName( sys._getframe().f_code.co_name )
                
        TEST_INVALID_JSON = {
                    "name": "t1",
                    "code": "123"
                }
        response = client.post("/api/boards/",json=TEST_INVALID_JSON)
        assert response.status_code == 422
    
    def test_GivenBoardIdExpectDeletionReturn204(self):
        testutilities.printTestCaseName( sys._getframe().f_code.co_name )
        
        NEW_JSON = {
            "name": "t3"
        }
        
        res = client.post("/api/boards/",json=NEW_JSON)
        boardId = res.json()["board"]["id"]
        
        
        response = client.delete("/api/boards/"+boardId)
        assert response.status_code == 204
        
        response = client.get("api/boards/")
        assert response.status_code == 200
        assert response.json()["results"] == 1
        
        

if __name__ == '__main__':
    unittest.main()