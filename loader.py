from loguru import logger
from requester import Requester
from settings import user_agent
from db import DataBase

import sys

# logger.remove()
logger.add('debug.log', format="{time} {level} {message}", level="DEBUG", rotation='1 day')
# logger.add(sys.stdout, format="<green>{time}</green> <white>{level}</white> <level>{message}</level>", level="INFO", colorize=True)

requester = Requester(user_agent)
db = DataBase()