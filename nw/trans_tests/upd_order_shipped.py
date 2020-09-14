from datetime import datetime

from sqlalchemy import inspect, MetaData
from sqlalchemy.ext.declarative import declarative_base

import nw.nw_logic.models as models
from logic_engine.exec_row_logic.logic_row import LogicRow
from logic_engine.util import row_prt, prt
from nw import nw_logic
from nw.nw_logic import session  # opens db, activates logic listener <--


""" toggle Shipped Date, to trigger balance adjustment """
""" also test join.
session.query(Customer).join(Invoice).filter(Invoice.amount == 8500).all()
"""

pre_cust = session.query(models.Customer).filter(models.Customer.Id == "ALFKI").one()
session.expunge(pre_cust)

print("")
test_order = session.query(models.Order).filter(models.Order.Id == 11011).join(models.Employee).one()
if test_order.ShippedDate is None or test_order.ShippedDate == "":
    test_order.ShippedDate = str(datetime.now())
    print(prt("Shipping order - ShippedDate: ['' -> " + test_order.ShippedDate + "]"))
else:
    test_order.ShippedDate = None
    print(prt("Returning order - ShippedDate: [ -> None]"))
insp = inspect(test_order)
session.commit()

print("")
post_cust = session.query(models.Customer).filter(models.Customer.Id == "ALFKI").one()
logic_row = LogicRow(row=pre_cust, old_row=post_cust, nest_level=0, ins_upd_dlt="*", a_session=session)

if abs(post_cust.Balance - pre_cust.Balance) == 960:
    logic_row.log("Correct adjusted Customer Result")
    assert True
else:
    row_prt(post_cust, "\nERROR - incorrect adjusted Customer Result")
    print("\n--> probable cause: Order customer update not written")
    row_prt(pre_cust, "\npre_cust")
    assert False

print("\nupd_order_shipped, ran to completion")


