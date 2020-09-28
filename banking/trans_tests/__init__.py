print("   ************** trans_tests MODULE INIT (never seems to run)  ************")

import os
import sys
from datetime import datetime

from sqlalchemy import inspect, MetaData
from sqlalchemy.ext.declarative import declarative_base

cwd = os.getcwd()   # eg, /Users/val/python/pycharm/python-rules/nw/trans_tests
path_python_rules = cwd  # seeking /Users/val/python/pycharm/python-rules
path_python_rules = path_python_rules.replace("/banking/trans_tests", "")
print("path: " + path_python_rules)

sys_path = ""
found = False
for each_node in sys.path:
    sys_path += each_node + "\n"
    if each_node == path_python_rules:
        found = True

if not found:
    print("Fixing path")
    sys.path.append(path_python_rules)

path_info = "Run Environment info...\n\n"\
            + "Current Working Directory: " + cwd + "\n\n"\
            + "sys.path: (Python imports)\n" + sys_path + "\n"\
            + "From: " + sys.argv[0] + "\n\n"\
            + "Using Python: " + sys.version + "\n\n"\
            + "At: " + str(datetime.now()) + "\n\n"
print("\n" + path_info + "\n\n")
