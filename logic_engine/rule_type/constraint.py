from typing import Callable

import logic_engine.exec_row_logic.logic_row as LogicRow

from logic_engine.rule_bank.rule_bank import RuleBank
from logic_engine.rule_type.rule import Rule


class Constraint(Rule):

    _function = None

    def __init__(self, validate: str,
                 error_msg: str,
                 calling: Callable = None,
                 as_condition: str = None):
        super(Constraint, self).__init__(validate)
        # self.table = validate  # setter finds object
        self._error_msg = error_msg
        self._as_condition = as_condition
        if calling is None and as_condition is None:
            raise Exception(f'Constraint {str} requires calling or as_expression')
        if calling is not None and as_condition is not None:
            raise Exception(f'Constraint {str} either calling or as_expression')
        if calling is not None:
            self._function = calling
        else:
            self._as_condition = lambda row: eval(as_condition)
        ll = RuleBank()
        ll.deposit_rule(self)

    def __str__(self):
        return f'Constraint Function: {str(self._function)} '

    def execute(self, logic_row: LogicRow):
        # logic_row.log(f'Constraint BEGIN {str(self)} on {str(logic_row)}')
        if self._function is not None:
            value = self._function(row=logic_row.row, old_row=logic_row.old_row, logic_row=logic_row)
        else:
            value = self._as_condition(row=logic_row.row)
        if value:
            pass
        elif not value:
            row = logic_row.row
            msg = eval(f'f"""{self._error_msg}"""')
            raise Exception("Constraint failed: " + msg)
        else:
            raise Exception(f'Constraint did not return boolean: {str(self)}')
        print(f'Constraint END {str(self)} on {str(logic_row)}')
