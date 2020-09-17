from typing import Callable

from sqlalchemy.orm.attributes import InstrumentedAttribute

from logic_engine.rule_type.constraint import Constraint
from logic_engine.rule_type.copy import Copy
from logic_engine.rule_type.count import Count
from logic_engine.rule_type.formula import Formula
from logic_engine.rule_type.row_event import EarlyRowEvent
from logic_engine.rule_type.sum import Sum


class Rule:
    """Invoke these functions to *define* rules.
    Rules are *not* run as they are defined,
    they are run when you issue `session.commit()'.
    Use code completion to discover rules.
    """

    @staticmethod
    def sum(derive: InstrumentedAttribute, as_sum_of: any, where: any = None):
        """
        Derive parent column as sum of designated child column, optional where, eg
          Rule.sum(derive=Customer.Balance, as_sum_of=Order.AmountTotal,
                   where=Lambda row: row.ShippedDate is None)
        Optimized to eliminate / minimize SQLs: Pruning, Adjustment Logic
        """
        Sum(derive, as_sum_of, where)

    @staticmethod
    def count(derive: InstrumentedAttribute, as_count_of: str, where: any = None):
        """
        Derive parent column as count of designated child rows, eg
          Rule.count(derive=Customer.UnPaidOrders, as_count_of=Order,
                   where=Lambda row: row.ShippedDate is None)
        Optimized to eliminate / minimize SQLs: Pruning, Adjustment Logic
        """
        Count(derive, as_count_of, where)

    @staticmethod
    def constraint(validate: object, as_condition: any = None,
                   error_msg: str = "(error_msg not provided)", calling: Callable = None):
        """
        Constraints declare condition that must be true for all commits, eg
          Rule.constraint(validate=Customer, as_condition=lambda row: row.Balance <= row.CreditLimit,
                          error_msg="balance ({row.Balance}) exceeds credit ({row.CreditLimit})")
        """
        Constraint(validate=validate, calling=calling, as_condition=as_condition, error_msg=error_msg)  # --> load_logic

    @staticmethod
    def early_row_event(on_class: str, calling: Callable = None):
        """
        Row Events are Python functions called before logic
        """
        EarlyRowEvent(on_class, calling)  # --> load_logic

    @staticmethod
    def formula(derive: InstrumentedAttribute, calling: Callable = None,
                as_expression: Callable = None, as_exp: str = None):
        """
        Formulas declare column value, based on current and parent rows, eg
          <code>Rule.formula(derive=OrderDetail.Amount,
                       as_expression=lambda row: row.UnitPrice * row.Quantity)</code>
        Unlike Copy rules, Parent changes are propagated to child row(s)
        Supply 1 (one) of the following:
          * as_exp - string (for very short expressions - price * quantity)
          * ex_expression - lambda (for type checking)
          * calling - function (for more complex formula, with old_row)
        """
        Formula(derive=derive, calling=calling, as_exp=as_exp, as_expression=as_expression)

    @staticmethod
    def copy(derive: InstrumentedAttribute, from_parent: any):
        """
        Copy declares child column copied from parent column, eg
          Rule.copy(derive=OrderDetail.UnitPrice, from_parent=Product.UnitPrice)
        Unlike formulas references, parent changes are *not* propagated to children
        """
        Copy(derive=derive, from_parent=from_parent)
