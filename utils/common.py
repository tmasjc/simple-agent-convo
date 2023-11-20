import sys
import configparser
from loguru import logger

config = configparser.ConfigParser()
config.read('config.ini')

logger.add(sys.stdout, level="TRACE")