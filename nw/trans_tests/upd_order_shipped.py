from datetime import datetime

from sqlalchemy import inspect

import nw.nw_logic.models as models
from logic_engine.exec_row_logic.logic_row import LogicRow
from nw.nw_logic import session  # opens db, activates logic listener <--


""" toggle Shipped Date, to trigger balance adjustment """
""" also test join.
session.query(Customer).join(Invoice).filter(Invoice.amount == 8500).all()
"""
pre_cust = session.query(models.Customer).filter(models.Customer.Id == "ALFKI").one()
session.expunge(pre_cust)

test_order = session.query(models.Order).filter(models.Order.Id == 11011).join(models.Employee).one()
if test_order.ShippedDate is None or test_order.ShippedDate == "":
    test_order.ShippedDate = str(datetime.now())
    print("shipping: ['' -> " + test_order.ShippedDate + "]")
else:
    test_order.ShippedDate = ""
    print("returning ['xxx' -> " + test_order.ShippedDate + "]")
# ship this unshipped order (dates are like 2014-03-24)
# a_session.query(models.Order).update(test_order)  # Order not iterable
insp = inspect(test_order)
session.commit()

post_cust = session.query(models.Customer).filter(models.Customer.Id == "ALFKI").one()
logic_row = LogicRow(row=pre_cust, old_row=post_cust, nest_level=0, ins_upd_dlt="*")
debug = logic_row.__str__()
print("Customer LogicRow: " + debug)
print("\nupd_order, completed\n\n")
# TODO check Customer Balance correctly adjusted

