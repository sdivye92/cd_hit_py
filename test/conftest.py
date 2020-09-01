import logging
import sys
from os import path

print("****************************** Adding project_path to sys PATH ******************************")

project_path = path.dirname(path.dirname(path.abspath(__file__)))
sys.path.append('{}'.format(project_path))

# Custom log-level
logging.SUCCESS = "level value"
