import sqlalchemy
from sqlalchemy.orm.attributes import InstrumentedAttribute

from logic_engine.exec_row_logic.logic_row import ParentRoleAdjuster
from logic_engine.rule_bank.rule_bank import RuleBank
from logic_engine.rule_type.aggregate import Aggregate


class Count(Aggregate):

    def __init__(self, derive: InstrumentedAttribute, as_count_of: object, where: any):
        super(Count, self).__init__(derive=derive, where=where)

        if not isinstance(as_count_of, sqlalchemy.ext.declarative.api.DeclarativeMeta):
            raise Exception("rule definition error, not mapped class: " + str(as_count_of))
        self._as_count_of = as_count_of
        self._as_count_of_class_name = self.get_class_name(as_count_of)

        rb = RuleBank()
        rb.deposit_rule(self)

    def __str__(self):
        if self._where != "":
            result = super().__str__() + f'Count({self._as_count_of} Where {self._where})'
        else:
            result = super().__str__() + f'Count({self._as_count_of})'
        return result

    def adjust_parent(self, parent_adjustor: ParentRoleAdjuster):
        """
        @see LogicRow.adjust_parent_aggregates
        Set parent_adjustor iff adjustment update is required for this aggregate
            * Insert & Delete - value non-zero
            * Update - summed field, where or pk changes
        if set, the parent will be updated (for possibly multiple adjusts for this role)
        """
        self.adjust_parent_aggregate(parent_adjustor=parent_adjustor,
                                     get_summed_field=lambda: 1,
                                     get_old_summed_field=lambda: 1
                                     )

