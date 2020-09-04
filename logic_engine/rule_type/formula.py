from typing import Callable

from logic_engine.exec_row_logic.logic_row import LogicRow
from logic_engine.rule_bank.rule_bank import RuleBank
from logic_engine.rule_type.derivation import Derivation


class Formula(Derivation):

    def __init__(self, derive: str, calling: Callable):
        super(Formula, self).__init__(derive)
        self._function = calling
        rb = RuleBank()
        rb.deposit_rule(self)

    def execute(self, logic_row: LogicRow):
        print(f'Formula BEGIN {str(self)} on {str(logic_row)}')
        value = self._function(row=logic_row.row, old_row=logic_row.old_row, logic_row=logic_row)
        setattr(logic_row.row, self._column, value)
        print(f'Formula END {str(self)} on {str(logic_row)}')

    def __str__(self):
        return super().__str__() + \
               f'Formula Function: {self._function} '
