from sqlalchemy.orm import RelationshipProperty
from sqlalchemy.orm.attributes import InstrumentedAttribute
from typing import Callable

from logic_engine.exec_row_logic.logic_row import ParentRoleAdjuster
from logic_engine.rule_bank.rule_bank import RuleBank
from logic_engine.rule_type.aggregate import Aggregate


class Sum(Aggregate):

    def __init__(self, derive: InstrumentedAttribute, as_sum_of: any, where: any):
        super(Sum, self).__init__(derive=derive, where=where)
        self._as_sum_of = as_sum_of  # could probably super-ize parent accessor
        if isinstance(as_sum_of, str):
            self._child_role_name = self._as_sum_of.split(".")[0]  # child role retrieves children
            self._child_summed_field = self._as_sum_of.split(".")[1]
        elif isinstance(as_sum_of, InstrumentedAttribute):
            self._child_summed_field = as_sum_of.key
            attrs = as_sum_of.parent.attrs
            found_attr = None
            for each_attr in attrs:
                if isinstance(each_attr, RelationshipProperty):
                    pass
                    parent_class_nodal_name = each_attr.entity.class_
                    parent_class_name = self.get_class_name(parent_class_nodal_name)
                    if parent_class_name == self.table:
                        if found_attr is not None:
                            raise Exception("TODO - disambiguate relationship")
                        found_attr = each_attr
            if found_attr is None:
                raise Exception("Invalid 'as_sum_of' - not a reference to: " + self.table +
                                " in " + self.__str__())
            else:
                self._child_role_name = found_attr.back_populates
        else:
            raise Exception("as_sum_of must be either string, or <mapped-class.column>: " +
                            str(as_sum_of))
        rb = RuleBank()
        rb.deposit_rule(self)

    def __str__(self):
        if self._where != "":
            result = super().__str__() + f'Sum({self._as_sum_of} Where {self._where})'
        else:
            result = super().__str__() + f'Sum({self._as_sum_of})'
        # result += "  (adjust using parent_role_name: " + self._parent_role_name + ")"
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
                                     get_summed_field=lambda: getattr(parent_adjustor.child_logic_row.row, self._child_summed_field),
                                     get_old_summed_field=lambda: getattr(parent_adjustor.child_logic_row.old_row, self._child_summed_field)
                                     )
