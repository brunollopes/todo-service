import jsonschema 
import json
import os
import jsonschema
from ..utils import util

log = util.getLog(__name__)

cwd = os.getcwd()  # Get the current working directory (cwd)
files = os.listdir(cwd)  # Get all the files in that directory
print("Files in %r: %s" % (cwd, files))


# Opening JSON file
f = open('server/app/resources/boardschema.json') 

schema = json.load(f)

def board_validate(board):
    log.info("given: "+ str(board))
    try:
        return jsonschema.validate(board, schema)
    except jsonschema.exceptions.ValidationError as err:
        print(err.message)
        return False
    