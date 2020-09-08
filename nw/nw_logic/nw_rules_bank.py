from logic_engine.logic import Logic
from logic_engine.rule_bank.rule_bank import RuleBank
from nw.nw_logic import models


def check_balance(row, old_row, logic_row) -> bool:
    return row.balance <= row.creditLimit


def compute_amount(row, old_row, logic_row):
    return row.UnitPrice * row.Quantity


def my_early_event(row, old_row, logic_row):
    logic_row.log("early event - good breakpoint, time/date stamping, etc")
    """You can get parent rows, like this
    emp_id = row.EmployeeId
    test_rep = logic_row.session.query(models.Employee).filter(models.Employee.Id == emp_id).one()
    print("can we assign the SalesRep??")
    """


Logic.constraint_rule(validate="Customer",
                      as_condition="row.Balance <= row.CreditLimit",
                      error_msg="balance ({row.Balance}) exceeds credit ({row.CreditLimit})")
Logic.sum_rule(derive="Customer.Balance", as_sum_of="OrderList.AmountTotal",
               where="row.ShippedDate is None")

Logic.sum_rule(derive="Order.AmountTotal", as_sum_of="OrderDetailList.Amount")

Logic.formula_rule(derive="OrderDetail.Amount",  # or, calling=compute_amount)
                   as_exp="row.UnitPrice * row.Quantity")
Logic.copy_rule(derive="OrderDetail.UnitPrice", from_parent="ProductOrdered.UnitPrice")


Logic.constraint_rule(validate="AbUser",  # table is ab_user
                      as_condition=lambda row: row.username != "noname")

Logic.count_rule(derive="Customer.OrderCount", as_count_of="Order",
                 where="ShippedDate not None")

Logic.early_row_event_rule(on_class="*", calling=my_early_event)


"""
alternate form for formulas, constraints:
    Logic.formula_rule(derive="OrderDetail.Amount", calling=compute_amount)
"""