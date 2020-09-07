from logic_engine.logic import Logic
from logic_engine.rule_bank.rule_bank import RuleBank


def check_balance(row, old_row, logic_row) -> bool:
    return row.balance <= row.creditLimit


def compute_amount(row, old_row, logic_row):
    return row.UnitPrice * row.Quantity


Logic.constraint_rule(validate="Customer",
                      as_condition="row.Balance <= row.CreditLimit")
Logic.sum_rule(derive="Customer.Balance", as_sum_of="OrderList.AmountTotal",
               where="row.ShippedDate is None")
Logic.count_rule(derive="Customer.OrderCount", as_count_of="Order", where="ShippedDate not None")

Logic.sum_rule(derive="Order.AmountTotal", as_sum_of="OrderDetailList.Amount")

Logic.formula_rule(derive="OrderDetail.Amount",
                   as_exp="row.UnitPrice * row.Quantity")
Logic.copy_rule(derive="OrderDetail.UnitPrice", from_parent="ProductOrdered.UnitPrice")


Logic.constraint_rule(validate="AbUser",  # table is ab_user
                      as_condition=lambda row: row.username != "noname")

rule_bank = RuleBank()
rule_bank.validate()

"""
alternate form for formulas, constraints:
    Logic.formula_rule(derive="OrderDetail.Amount", calling=compute_amount)
"""