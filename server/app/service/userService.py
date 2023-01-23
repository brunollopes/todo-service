import random
import requests
from ..utils import util

log = util.getLog(__name__)

API_URL="https://randomuser.me/api/?results=10&seed=123"

def get_randomUser():
    pos = random.randint(0, 9)
    users = requests.get(API_URL).json()["results"]
    print(users[pos])
    return users[pos]

def get_user_by_uuid(uuid):
    log.info("given: "+ str(uuid))
    users = requests.get(API_URL).json()["results"]
    for user in users:
        userUUId = user["login"]["uuid"]
        if str(userUUId) == uuid:
            return user 
    return None
    