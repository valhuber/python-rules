from sqlalchemy.orm import object_mapper

from logic_engine.exec_row_logic.logic_row import LogicRow
from logic_engine.exec_row_logic.parent_role_adjuster import ParentRoleAdjuster
from logic_engine.rule_type.derivation import Derivation


class Aggregate(Derivation):

    def __init__(self, derive: str):
        super(Aggregate, self).__init__(derive)

    def adjust_parent(self, a_parent_adjustor: ParentRoleAdjuster):
        raise Exception("Not implemented - subclass responsibility")

    def get_parent_role_from_child_role_name(self,
                                             child_logic_row: LogicRow,
                                             child_role_name: str) -> str:
        my_mapper = object_mapper(child_logic_row.row)
        role_def = my_mapper.relationships.get(child_role_name)


