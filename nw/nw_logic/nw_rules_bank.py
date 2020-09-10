from logic_engine.logic import Logic
from logic_engine.rule_bank.rule_bank import RuleBank
from nw.nw_logic import models

"""
Rules (below) can invoke Python functions
"""
def check_balance(row, old_row, logic_row) -> bool:
    """
    Not used... illustrate function alternative (e.g., more complex if/else logic)
    specify rule with `calling=check_balance` (instead of as_condition)
    """
    return row.balance <= row.creditLimit


def compute_amount(row, old_row, logic_row):
    """
    Not used... illustrate function alternative (e.g., more complex if/else logic)
    """
    return row.UnitPrice * row.Quantity


def my_early_event(row, old_row, logic_row):
    logic_row.log("early event for *all* tables - good breakpoint, time/date stamping, etc")


"""
These rules apply to all transactions, automatically, eg.
* place order
* change Order Detail product, amount
* add/delete Order Detail
* ship / unship order
* delete order
* move order to new customer
* etc
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

Dependency Graph test (internal use only, please ignore):

Logic.formula_rule(derive="Tbl.ColA",  # or, calling=compute_amount)
                   as_exp="row.ColB + row.ColC")

Logic.formula_rule(derive="Tbl.ColB",  # or, calling=compute_amount)
                   as_exp="row.ColC")

Logic.formula_rule(derive="Tbl.ColC",  # or, calling=compute_amount)
                   as_exp="row.ColD")

Logic.formula_rule(derive="Tbl.ColD",  # or, calling=compute_amount)
                   as_exp="row.ColE")

Logic.formula_rule(derive="Tbl.ColE",  # or, calling=compute_amount)
                   as_exp="xxx")

"""