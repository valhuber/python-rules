import os
import sqlalchemy
import nw.nw_logic.models as models
from nw.nw_logic import session  # opens db, activates logic listener <--


# first delete, so can add
delete_cust = session.query(models.Customer).filter(models.Customer.Id == "$$New Cust").delete()
print("\nadd_cust, deleting: " + str(delete_cust) + "\n\n")
session.commit()

# Add a Customer - works
new_cust = models.Customer(Id="$$New Cust", )
session.add(new_cust)
session.commit()

verify_cust = session.query(models.Customer).filter(models.Customer.Id == "$$New Cust").one()

print("\nadd_cust, completed: " + str(verify_cust) + "\n\n")

assert True
