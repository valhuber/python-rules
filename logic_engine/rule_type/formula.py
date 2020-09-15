import inspect
from typing import Callable

import logic_engine.exec_row_logic.logic_row as LogicRow
from logic_engine.rule_bank.rule_bank import RuleBank
from logic_engine.rule_type.derivation import Derivation


class Formula(Derivation):

    def __init__(self, derive: str,
                 calling: Callable = None,
                 as_exp: str = None):
        super(Formula, self).__init__(derive)
        self._function = calling
        self._as_exp = as_exp
        self._as_exp_lambda = None
        if as_exp is not None:
            self._as_exp_lambda = lambda row: eval(as_exp)
        if self._function is None and self._as_exp is None:
            raise Exception(f'Formula {str} requires calling or as_exp')
        if self._function is not None and self._as_exp is not None:
            raise Exception(f'Formula {str} requires *either* calling or as_expression')
        self._dependencies = []
        text = self.get_rule_text()
        self.parse_dependencies(rule_text=text)
        self._exec_order = -1  # will be computed in rule_bank_setup (all rules loaded)
        rb = RuleBank()
        rb.deposit_rule(self)

    def execute(self, logic_row: LogicRow):
        """
        executes EITHER:
          - as_exp_lambda(row=logic_row.row), OR
          - _function(row, old_row, logic_row)
        """
        # logic_row.log(f'Formula BEGIN {str(self)} on {str(logic_row)}')
        if self._function is not None:
            value = self._function(row=logic_row.row,
                                   old_row=logic_row.old_row, logic_row=logic_row)
        elif self._as_exp_lambda is not None:
            value = self._as_exp_lambda(row=logic_row.row)
        else:
            value = self._as_exp(row=logic_row.row)
        old_value = getattr(logic_row.row, self._column)
        if value != old_value:
            setattr(logic_row.row, self._column, value)
            logic_row.log(f'Formula {self._column}')

    def get_rule_text(self):
        text = self._as_exp
        if self._as_exp is None:
            text = inspect.getsource(self._function)
        return text

    def __str__(self):  # TODO get text of as_expression
        return super().__str__() + \
               f'Formula ({self._exec_order}) Function: {self._function} '
