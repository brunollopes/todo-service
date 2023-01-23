import json
import unittest
from app.tests import testutilities
from app.validators import board_validator
import sys
 
PRINT = True            # change to False when finished debugging...
GOOD_JSON = '{"id":"9c5ea47a-3118-42c4-d9e3-75903a0a6d4e","name":"ullamco ex enim dolor","description":"ullamco incididunt","tasks":[{"id":"ba21d45d-11e2-9930-7d82-ce24b3847342","name":"Ut ex","user":"bb13a758-4dc1-e9f8-bfcd-244f337a26a2","description":"irure minim","status":"Started"}]}'
BAD_JSON  = '{"id":"9c5ea47a-3118-42c4-d9e3-75903a0a6d4e","description":"ullamco incididunt","tasks":[{"id":"ba21d45d-11e2-9930-7d82-ce24b3847342","name":"Ut ex","user":"bb13a758-4dc1-e9f8-bfcd-244f337a26a2","description":"irure minim","status":"Started"}]}'

class TestBoardSchemaValidator (unittest.TestCase):
    
    @classmethod
    def setUpClass( JsonValidateTest ):
        testutilities.turnOnPrinting( PRINT )
    
    def setUp( self ):
        pass

    def tearDown( self ):
        pass

    def test_ThatGivenAValidJsonDataReturnsTrue( self):
        testutilities.printTestCaseName( sys._getframe().f_code.co_name )
        data = json.loads(GOOD_JSON)
        
        res = board_validator.board_validate(data)
        self.assertIsNone( res )
        
    def test_ThatGivenAnInValidJsonDataReturnsFalse( self):
        testutilities.printTestCaseName( sys._getframe().f_code.co_name )
        data = json.loads(BAD_JSON)
        
        res = board_validator.board_validate(data)
        self.assertFalse( res )

if __name__ == '__main__':
    unittest.main()