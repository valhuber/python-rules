"""
PyCharm sets PythonPath to the root folder, VSC does not by default - imports fail
Hence, add this to the launch config:
"env": {"PYTHONPATH": "${workspaceFolder}:${env:PYTHONPATH}"}

ref: https://stackoverflow.com/questions/53653083/how-to-correctly-set-pythonpath-for-visual-studio-code
"""

import os
import sys
from datetime import datetime
from decimal import Decimal

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


""" 
Illustrate re-use with a number of changes:
    1 - reassign the order to a different customer
    2 - change an OrderDetail (eg, "I'll buy 1 WidgetSet, not 5 Widgets")
        a. A different Product
        b. A different Quantity
"""

pre_alfki = session.query(models.Customer).filter(models.Customer.Id == "ALFKI").one()
pre_anatr = session.query(models.Customer).filter(models.Customer.Id == "ANATR").one()

logic_row = LogicRow(row=pre_alfki, old_row=pre_alfki,
                     ins_upd_dlt="*", nest_level=0, a_session=session, row_sets=None)
logic_row.log("starting")

logic_row = LogicRow(row=pre_anatr, old_row=pre_anatr,
                     ins_upd_dlt="*", nest_level=0, a_session=session, row_sets=None)
logic_row.log("starting")

pre_order = session.query(models.Order).filter(models.Order.Id == 11011).one()  # type : Order
logic_row = LogicRow(row=pre_order, old_row=pre_order,
                     ins_upd_dlt="*", nest_level=0, a_session=session, row_sets=None)
logic_row.log("starting")
session.expunge(pre_alfki)
session.expunge(pre_anatr)
session.expunge(pre_order)

print("")

test_order = session.query(models.Order).filter(models.Order.Id == 11011).one()  # type : Order
test_order_details = test_order.OrderDetailList
changed_order_detail = None
for each_order_detail in test_order_details:
    if each_order_detail.ProductId == 58:  # Escargots de Bourgogne, @ $13.25
        each_order_detail.ProductId = 48   # Chocolade, @ $12.75
        each_order_detail.Quantity = 10    # 40 x 13.25 => 10 x 12.75
        break

pre_amount_total = test_order.AmountTotal
post_amount_total = pre_amount_total -\
                    Decimal(40.0) * Decimal(13.25) +\
                    Decimal(10.0) * Decimal(12.75)

test_order.CustomerId = "ANATR"

print("\n" + prt("Reparenting *altered* order - new CustomerId: " + test_order.CustomerId))
print(f'order amount {pre_amount_total} projected to be {post_amount_total}')
insp = inspect(test_order)

session.commit()
print('')

msg = 'Committed... order.amountTotal ' + \
      str(pre_amount_total) + ' -> ' + \
      str(post_amount_total)
logic_row = LogicRow(row=test_order, old_row=pre_order,
                     ins_upd_dlt="*", nest_level=0, a_session=session, row_sets=None)
logic_row.log(msg)
print("\n")


post_alfki = session.query(models.Customer).filter(models.Customer.Id == "ALFKI").one()
logic_row = LogicRow(row=post_alfki, old_row=pre_alfki,
                     ins_upd_dlt="*", nest_level=0, a_session=session, row_sets=None)

if post_alfki.Balance == 0:
    logic_row.log("Correct non-adjusted Customer Result")
    assert True
else:
    print("\n*** ERROR***")
    msg = "ERROR - incorrect adjusted Customer Result, " + "should be 0"
    logic_row.log(msg)
    assert False

post_anatr = session.query(models.Customer).filter(models.Customer.Id == "ANATR").one()
logic_row = LogicRow(row=post_anatr, old_row=pre_anatr,
                     ins_upd_dlt="*", nest_level=0, a_session=session, row_sets=None)

if post_anatr.Balance == 557.50:
    logic_row.log("Correct non-adjusted Customer Result")
    assert True
else:
    print("\n*** ERROR***")
    msg = "ERROR - incorrect adjusted Customer Result, " + "should be 557.50"
    logic_row.log(msg)
    assert False

print("\nupd_order_customer_reuse, ran to completion")


