from logic_engine.exec_row_logic.parent_role_adjuster import ParentRoleAdjuster
from logic_engine.rule_bank.rule_bank import RuleBank
from logic_engine.rule_type.aggregate import Aggregate


class Sum(Aggregate):

    _as_sum_of = ""
    _from_parent_role = ""
    _where = ""

    def __init__(self, derive: str, as_sum_of: str, where: str):
        super(Sum, self).__init__(derive)
        self._as_sum_of = as_sum_of  # could probably super-ize parent accessor
        self._from_parent_role = self._as_sum_of.split(".")[0]
        self._where = where
        if where is None:
            self._where_cond = lambda row: True
        else:
            self._where_cond = lambda row: eval(where)
        rb = RuleBank()
        rb.deposit_rule(self)

    def __str__(self):
        if self._where != "":
            result = super().__str__() + f'Sum({self._as_sum_of} Where {self._where})'
        else:
            result = super().__str__() + f'Sum({self._as_sum_of})'
        return result

    def adjust_parent(self, parent_adjustor: ParentRoleAdjuster):
        print(str(self))  # this is where the work is
        delta = 0.0
        if parent_adjustor.child_logic_row.ins_upd_dlt == "ins":
            where = self._where_cond(parent_adjustor.child_logic_row.row)
            delta = getattr(parent_adjustor.child_logic_row.row, self._column)
            if where and delta != 0.0:
                parent_role_name = self.get_parent_role_from_child_role_name(
                    child_logic_row = parent_adjustor.child_logic_row,
                    child_role_name = self._from_parent_role
                )
                parent_adjustor.parent_logic_row =\
                    parent_adjustor.child_logic_row.get_parent_logic_row(
                        role_name=self._from_parent_role)
                print(f'sum adjusts {str(self)}')
        elif parent_adjustor.child_logic_row.ins_upd_dlt == "dlt":
            raise Exception("sum / delete child not implemented")
        elif parent_adjustor.child_logic_row.ins_upd_dlt == "upd":
            raise Exception("sum / update child not implemented")
        else:
            raise Exception("system error - sum finds bad child ins_upd_dlt")


