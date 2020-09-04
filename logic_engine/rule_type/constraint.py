from logic_engine.exec_row_logic.logic_row import LogicRow
from logic_engine.rule_bank.rule_bank import RuleBank
from logic_engine.rule_type.rule import Rule


class Constraint(Rule):

    _function = None

    def __init__(self, validate: str, calling):
        super(Constraint, self).__init__(validate)
        # self.table = validate  # setter finds object
        self._function = calling
        ll = RuleBank()
        ll.deposit_rule(self)

    def __str__(self):
        return f'Constraint Function: {str(self._function)} '

    def execute(self, logic_row: LogicRow):
        print(f'Constraint BEGIN {str(self)} on {str(logic_row)}')
        value = self._function(row=logic_row.row, old_row=logic_row.old_row, logic_row=logic_row)
        if value:
            pass
        elif not value:
            raise Exception(f'Constraint fails: {str(self)}')
        else:
            raise Exception(f'Constraint did not return boolean: {str(self)}')
        print(f'Constraint END {str(self)} on {str(logic_row)}')
