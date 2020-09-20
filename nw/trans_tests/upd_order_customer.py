"""
PyCharm sets PythonPath to the root folder, VSC does not by default - imports fail
Hence, add this to the launch config:
"env": {"PYTHONPATH": "${workspaceFolder}:${env:PYTHONPATH}"}

ref: https://stackoverflow.com/questions/53653083/how-to-correctly-set-pythonpath-for-visual-studio-code
"""

import os
import sys
from datetime import datetime

from sqlalchemy import inspect, MetaData
from sqlalchemy.ext.declarative import declarative_base

cwd = os.getcwd()   # eg, /Users/val/python/pycharm/python-rules/nw/trans_tests
required_path_python_rules = cwd  # seeking /Users/val/python/pycharm/python-rules
required_path_python_rules = required_path_python_rules.replace("/nw/trans_tests", "")

sys_path = ""
required_path_present = False
for each_node in sys.path:
    sys_path += each_node + "\n"
    if each_node == required_path_python_rules:
        required_path_present = True

if not required_path_present:
    print("Fixing path (so can run from terminal)")
    sys.path.append(required_path_python_rules)
else:
    pass
    print("NOT Fixing path (default PyCharm, set in VSC Launch Config)")

path_info = "Run Environment info...\n\n"\
            + "Current Working Directory: " + cwd + "\n\n"\
            + "sys.path: (Python imports)\n" + sys_path + "\n"\
            + "From: " + sys.argv[0] + "\n\n"\
            + "Using Python: " + sys.version + "\n\n"\
            + "At: " + str(datetime.now()) + "\n\n"
print("\n" + path_info + "\n\n")


import nw.nw_logic.models as models
from logic_engine.exec_row_logic.logic_row import LogicRow
from logic_engine.util import row_prt, prt
from nw import nw_logic
from nw.nw_logic import session  # opens db, activates logic listener <--


""" toggle order's customer to ANATR, to verify no effect on Customer, OrderDetails """

pre_alfki = session.query(models.Customer).filter(models.Customer.Id == "ALFKI").one()
pre_anatr = session.query(models.Customer).filter(models.Customer.Id == "ANATR").one()
session.expunge(pre_alfki)
session.expunge(pre_anatr)

print("")
test_order = session.query(models.Order).filter(models.Order.Id == 11011).one()  # type : Order
amount_total = test_order.AmountTotal
if test_order.CustomerId  == "ALFKI":
    test_order.CustomerId = "ANATR"
else:
    test_order.CustomerId = "ALFKI"
print(prt("Reparenting order - new CustomerId: " + test_order.CustomerId))
insp = inspect(test_order)
session.commit()

print("")
post_alfki = session.query(models.Customer).filter(models.Customer.Id == "ALFKI").one()
logic_row = LogicRow(row=pre_alfki, old_row=post_alfki, ins_upd_dlt="*", nest_level=0, a_session=session, row_cache=None)

if abs(post_alfki.Balance - pre_alfki.Balance) == 960:
    logic_row.log("Correct non-adjusted Customer Result")
    assert True
else:
    row_prt(post_alfki, "\nERROR - incorrect adjusted Customer Result")
    print("\n--> probable cause: Order customer update not written")
    row_prt(pre_alfki, "\npre_alfki")
    assert False

post_anatr = session.query(models.Customer).filter(models.Customer.Id == "ANATR").one()
logic_row = LogicRow(row=pre_anatr, old_row=post_alfki, ins_upd_dlt="*", nest_level=0, a_session=session, row_cache=None)

if abs(post_anatr.Balance - pre_anatr.Balance) == 960:
    logic_row.log("Correct non-adjusted Customer Result")
    assert True
else:
    row_prt(post_anatr, "\nERROR - incorrect adjusted Customer Result")
    print("\n--> probable cause: Order customer update not written")
    row_prt(pre_anatr, "\npre_anatr")
    assert False

print("\nupd_order_customer, ran to completion")


