import sys
import configparser
from loguru import logger
import redis

# read configuration
config = configparser.ConfigParser()
config.read("config.ini")

# set logging level
logger.add(sys.stdout, level="TRACE")

# connect to Redis
r = config["REDIS"]
redis_client = redis.Redis(host=r["host"], port=r["port"], db=r["db"])

