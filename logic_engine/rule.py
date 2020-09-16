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
    """

    @staticmethod
    def sum(derive: InstrumentedAttribute, as_sum_of: str, where: str = None):
        """
        Sums declare parent column as sum of designated child column
        Optimized to eliminate / minimize SQLs: Pruning, Adjustment Logic
        """
        Sum(derive, as_sum_of, where)

    @staticmethod
    def count(derive: InstrumentedAttribute, as_count_of: str, where: str = ""):
        """
        Sums declare parent column as sum of designated child rows
        Optimized to eliminate / minimize SQLs: Pruning, Adjustment Logic
        """
        Count(derive, as_count_of, where)

    @staticmethod
    def constraint(validate: object, as_condition: any = None,
                   error_msg: str = "(error_msg not provided)", calling: Callable = None):
        """
        Constraints declare condition that must be true for all commits
        """
        Constraint(validate=validate, calling=calling, as_condition=as_condition, error_msg=error_msg)  # --> load_logic

    @staticmethod
    def early_row_event(on_class: str, calling: Callable = None):
        """
        Row Events are Python functions called before/after logic
        """
        EarlyRowEvent(on_class, calling)  # --> load_logic

    @staticmethod
    def formula(derive: InstrumentedAttribute, calling: Callable = None,
                as_expression: Callable = None, as_exp: str = None):
        """
        Formulas declare column value, based on current and parent rows
        Parent changes are propagated to child row(s)
        Supply 1 (one) of the following:
          * as_exp - string (for very short expressions - price * quantity)
          * ex_expression - lambda (for type checking)
          * calling - function (for more complex formula, with old_row)
        """
        Formula(derive=derive, calling=calling, as_exp=as_exp, as_expression=as_expression)

    @staticmethod
    def copy(derive: InstrumentedAttribute, from_parent: str):
        """
        Copy declares child column copied from parent column
        Unlike formulas references, parent changes are *not* propagated to children
        """
        Copy(derive=derive, from_parent=from_parent)
