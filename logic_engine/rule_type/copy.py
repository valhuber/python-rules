from sqlalchemy.orm.attributes import InstrumentedAttribute

import logic_engine.exec_row_logic.logic_row as LogicRow
from logic_engine.rule_bank.rule_bank import RuleBank
from logic_engine.rule_type.derivation import Derivation


class Copy(Derivation):

    def __init__(self, derive: InstrumentedAttribute, from_parent: str):
        super(Copy, self).__init__(derive)
        names = from_parent.split('.')
        self._from_parent_role = names[0]
        self._from_column = names[1]
        rb = RuleBank()
        rb.deposit_rule(self)

    def execute(self, child_logic_row: LogicRow, parent_logic_row: LogicRow):
        each_column_value = getattr(parent_logic_row.row, self._from_column)
        setattr(child_logic_row.row, self._column, each_column_value)

    def __str__(self):
        return super().__str__() + \
               f'Copy({self._from_parent_role}.{self._from_column})'
