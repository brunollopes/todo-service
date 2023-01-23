import logging
from uuid import UUID
from ..logConfig import getLogHandler
from ..utils import util

def validate_uuidv4(uuid_str):
    getLog(__name__).info("given: "+ uuid_str)
    try:
        val = UUID(uuid_str, version=4)
    except ValueError:
        # If it's a value error, then the string 
        # is not a valid hex code for a UUID.
        return False
    return str(val) == uuid_str

def getLog(name):
    log = logging.getLogger(name)
    log.setLevel(logging.INFO)
    log.addHandler(getLogHandler())
    return log