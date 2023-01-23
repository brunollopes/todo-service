import logging
import logging.handlers
import os
import sys
 
def getLogHandler ():
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s')
    handler.setFormatter(formatter)
    return handler
