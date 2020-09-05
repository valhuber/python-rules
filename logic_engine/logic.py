from typing import Callable

from sqlalchemy.ext.declarative import declarative_base

from logic_engine.rule_type.constraint import Constraint
from logic_engine.rule_type.copy import Copy
from logic_engine.rule_type.count import Count
from logic_engine.rule_type.formula import Formula
from logic_engine.rule_type.sum import Sum

Base = declarative_base()
metadata = Base.metadata


class LogicContext:
    row = None
    old_row = None
    insert_update_delete = ""
    metadata = None
    nest_level = 0


class Logic:
    """Invoke these functions to *define* rules.
    Rules are *not* run as they are defined,
    they are run when you issue `session.commit()'.
    """

    @staticmethod
    def sum_rule(derive: str, as_sum_of: str, where: str = ""):
        """
        Sums declare parent column as sum of designated child column
        Optimized to eliminate / minimize SQLs: Pruning, Adjustment Logic
        """
        Sum(derive, as_sum_of, where)

    @staticmethod
    def count_rule(derive: str, as_count_of: str, where: str = ""):
        """
        Sums declare parent column as sum of designated child rows
        Optimized to eliminate / minimize SQLs: Pruning, Adjustment Logic
        """
        Count(derive, as_count_of, where)

    @staticmethod
    def constraint_rule(validate: str, calling: Callable = None, as_condition: Callable= None):
        """
        Constraints declare condition that must be true for all commits
        """
        Constraint(validate, calling, as_condition)  # --> load_logic

    @staticmethod
    def formula_rule(derive: str, calling: Callable = None, as_expression: Callable = None):
        """
        Formulas declare column value, based on current and parent rows
        Parent changes are propagated to child row(s)
        """
        Formula(derive=derive, calling=calling, as_expression=as_expression)

    @staticmethod
    def copy_rule(derive: str, from_parent: str):
        """
        Copy declares child column copied from parent column
        Unlike formulas references, parent changes are *not* propagated to children
        """
        Copy(derive=derive, from_parent=from_parent)

""""
class Constraint(Object):
    def __init__(self, row, old_row, logic_context: LogicContext):
        # exec code

class Sum(row: Base, old_row: Base, qual: bool):
    pass
"""