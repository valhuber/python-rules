from typing import Callable

import logic_engine.exec_row_logic.logic_row as LogicRow
from logic_engine.rule_bank.rule_bank import RuleBank
from logic_engine.rule_type.derivation import Derivation


class Formula(Derivation):

    def __init__(self, derive: str,
                 calling: Callable = None,
                 as_expression: Callable = None,
                 as_exp: str = None):
        super(Formula, self).__init__(derive)
        self._function = calling
        self._as_expression = as_expression
        self._as_exp = lambda row: eval(as_exp)
        """  TODO decide on exp vs expression, and activate these validations
        if self._function is None and self._as_expression is None:
            raise Exception(f'Formula {str} requires calling or as_expression')
        if self._function is not None and self._as_expression is not None:
            raise Exception(f'Formula {str} either calling or as_expression')
        """
        rb = RuleBank()
        rb.deposit_rule(self)

    def execute(self, logic_row: LogicRow):
        # logic_row.log(f'Formula BEGIN {str(self)} on {str(logic_row)}')
        if self._function is not None:
            value = self._function(row=logic_row.row,
                                   old_row=logic_row.old_row, logic_row=logic_row)
        elif self._as_expression is not None:
            value = self._as_expression(row=logic_row.row)
        else:
            value = self._as_exp(row=logic_row.row)
        old_value = getattr(logic_row.row, self._column)
        if value != old_value:
            setattr(logic_row.row, self._column, value)
            logic_row.log(f'Formula {str(self)}')

    def __str__(self):  # TODO get text of as_expression
        return super().__str__() + \
               f'Formula Function: {self._function} '
