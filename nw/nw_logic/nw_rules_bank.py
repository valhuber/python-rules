from logic_engine.exec_row_logic.logic_row import LogicRow
from logic_engine.logic import Logic
from logic_engine.rule_bank.rule_bank import RuleBank
from nw.nw_logic import models
from nw.nw_logic.models import Customer, OrderDetail, Product


def activate_basic_check_credit_rules():
    """
    Issues function calls to activate check credit rules, below.
        These rules are executed not now, but on commits
        Order is irrelevant - determined by system based on dependency analysis
        Their inclusion in classes is for doc / convenience, no semantics

    These rules apply to all transactions (automatic re-use), eg.
    * place order
    * change Order Detail product, quantity
    * add/delete Order Detail
    * ship / unship order
    * delete order
    * move order to new customer, etc
    """

    def units_shipped(row: Product, old_row: Product, logic_row: LogicRow):
        result = row.UnitsInStock - (row.UnitsShipped - old_row.UnitsOnOrder)
        return result

    Logic.constraint_rule(validate="Customer", as_condition="row.Balance <= row.CreditLimit",
                          error_msg="balance ({row.Balance}) exceeds credit ({row.CreditLimit})")
    Logic.sum_rule(derive="Customer.Balance", as_sum_of="OrderList.AmountTotal", where="row.ShippedDate is None")

    Logic.sum_rule(derive="Order.AmountTotal", as_sum_of="OrderDetailList.Amount")

    Logic.formula_rule(derive="OrderDetail.Amount",  as_exp="row.UnitPrice * row.Quantity")
    Logic.copy_rule(derive="OrderDetail.UnitPrice", from_parent="ProductOrdered.UnitPrice")
    Logic.formula_rule(derive="OrderDetail.ShippedDate", as_exp="row.OrderHeader.ShippedDate")

    Logic.sum_rule(derive="Product.UnitsShipped", as_sum_of="OrderDetails.Quantity",
                    where="row.ShippedDate is not None")
    Logic.formula_rule(derive="Product.UnitsShipped", as_expression=units_shipped)

class InvokePythonFunctions:  # use functions for more complex rules, type checking, etc (not used)

    @staticmethod
    def load_rules(self):

        def my_early_event(row, old_row, logic_row):
            logic_row.log("early event for *all* tables - good breakpoint, time/date stamping, etc")

        def check_balance(row: Customer, old_row, logic_row) -> bool:
            """
            Not used... illustrate function alternative (e.g., more complex if/else logic)
            specify rule with `calling=check_balance` (instead of as_condition)
            """
            return row.Balance <= row.CreditLimit

        def compute_amount(row: OrderDetail, old_row, logic_row):
            return row.UnitPrice * row.Quantity

        Logic.formula_rule(derive="OrderDetail.Amount", calling=compute_amount)

        Logic.formula_rule(derive="OrderDetail.Amount", calling=lambda Customer: Customer.Quantity * Customer.UnitPrice)

        Logic.early_row_event_rule(on_class="*", calling=my_early_event)  # just for debug

        Logic.constraint_rule(validate="Customer", calling=check_balance,
                              error_msg="balance ({row.Balance}) exceeds credit ({row.CreditLimit})")


class DependencyGraphTests:
    """Not loaded"""

    def not_loaded(self):
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


class UnusedTests:
    """Not loaded"""
    def not_loaded(self):
        Logic.constraint_rule(validate="AbUser",  # table is ab_user
                              calling=lambda row: row.username != "no_name")

        Logic.count_rule(derive="Customer.OrderCount", as_count_of="Order",
                         where="ShippedDate not None")
