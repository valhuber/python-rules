from sqlalchemy.orm import RelationshipProperty
from sqlalchemy.orm.attributes import InstrumentedAttribute
from typing import Callable

from logic_engine.exec_row_logic.logic_row import ParentRoleAdjuster
from logic_engine.rule_bank.rule_bank import RuleBank
from logic_engine.rule_type.aggregate import Aggregate


class Sum(Aggregate):
    _as_sum_of = ""
    _child_role_name = ""
    _where = ""

    def __init__(self, derive: InstrumentedAttribute, as_sum_of: any, where: any):
        super(Sum, self).__init__(derive)
        self._as_sum_of = as_sum_of  # could probably super-ize parent accessor
        self._where = where
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
        if where is None:
            self._where_cond = lambda row: True
        elif isinstance(where, str):
            self._where_cond = lambda row: eval(where)
        elif isinstance(where, Callable):
            self._where_cond = where
        else:
            raise Exception("'where' must be string, or lambda: " + self.__str__())
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
        # parent_adjustor.child_logic_row.log(str(self))  # this is where the work is
        delta = 0.0
        if parent_adjustor.child_logic_row.ins_upd_dlt == "ins":
            self.adjust_from_inserted_child(parent_adjustor)
        elif parent_adjustor.child_logic_row.ins_upd_dlt == "dlt":
            self.adjust_from_deleted_child(parent_adjustor)
        elif parent_adjustor.child_logic_row.ins_upd_dlt == "upd":
            self.adjust_from_updated_child(parent_adjustor)
        else:
            raise Exception("Internal error - unexpected ins_upd_dlt value")

    def adjust_from_inserted_child(self, parent_adjustor: ParentRoleAdjuster):
        delta = 0.0
        where = self._where_cond(parent_adjustor.child_logic_row.row)
        delta = getattr(parent_adjustor.child_logic_row.row, self._child_summed_field)
        if where and delta != 0.0:
            parent_role_name = self.get_parent_role_from_child_role_name(
                child_logic_row=parent_adjustor.child_logic_row,
                child_role_name=self._child_role_name
            )
            parent_adjustor.parent_logic_row = \
                parent_adjustor.child_logic_row.get_parent_logic_row(
                    role_name=self._parent_role_name)
            curr_value = getattr(parent_adjustor.parent_logic_row.row, self._column)
            setattr(parent_adjustor.parent_logic_row.row, self._column, curr_value + delta)
            # parent_adjustor.child_logic_row.log(f'adjust_from_inserted/adopted_child adjusts {str(self)}')

    def adjust_from_deleted_child(self, parent_adjustor: ParentRoleAdjuster):
        raise Exception("sum / update deleted child not implemented")
        delta = 0.0
        where = self._where_cond(parent_adjustor.child_logic_row.row)
        delta = getattr(parent_adjustor.child_logic_row.row, self._child_summed_field)
        if where and delta != 0.0:
            parent_role_name = self.get_parent_role_from_child_role_name(
                child_logic_row=parent_adjustor.child_logic_row,
                child_role_name=self._child_role_name
            )
            parent_adjustor.parent_logic_row = \
                parent_adjustor.child_logic_row.get_parent_logic_row(
                    role_name=self._parent_role_name, for_update=True)
            curr_value = getattr(parent_adjustor.parent_logic_row.row, self._column)
            setattr(parent_adjustor.parent_logic_row.row, self._column, curr_value + delta)
            # print(f'adjust_from_deleted/abandoned_child adjusts {str(self)}')

    def adjust_from_updated_child(self, parent_adjustor: ParentRoleAdjuster):
        delta = 0.0
        parent_role_name = parent_adjustor.parent_role_name
        if parent_adjustor.child_logic_row.is_different_parent(parent_role_name) is False:
            where = self._where_cond(parent_adjustor.child_logic_row.row)
            old_where = self._where_cond(parent_adjustor.child_logic_row.old_row)
            if where != False and where != True:
                raise Exception("where clause must return boolean: " +
                                str(where) + ", from " + self.__str__())
            delta = 0.0
            if where and old_where:
                delta = getattr(parent_adjustor.child_logic_row.row, self._child_summed_field) - \
                    getattr(parent_adjustor.child_logic_row.old_row, self._child_summed_field)
            elif not where and not old_where:
                delta = 0.0
            elif where:
                delta = getattr(parent_adjustor.child_logic_row.row, self._child_summed_field)
            else:
                delta = - getattr(parent_adjustor.child_logic_row.row, self._child_summed_field)

            if delta != 0.0:
                parent_role_name = self.get_parent_role_from_child_role_name(
                    child_logic_row=parent_adjustor.child_logic_row,
                    child_role_name=self._child_role_name
                )
                parent_adjustor.parent_logic_row = \
                    parent_adjustor.child_logic_row.get_parent_logic_row(
                        role_name=self._parent_role_name)
                curr_value = getattr(parent_adjustor.parent_logic_row.row, self._column)
                setattr(parent_adjustor.parent_logic_row.row, self._column, curr_value + delta)
                # parent_adjustor.child_logic_row.log(f'adjust_from_updated_child adjusts {str(self)}')
        else:
            raise Exception("TODO major sum / re-parent not implemented")
