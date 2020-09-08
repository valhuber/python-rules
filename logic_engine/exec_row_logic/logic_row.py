import sqlalchemy
import sqlalchemy_utils
from sqlalchemy.ext.declarative import base
from sqlalchemy.engine.reflection import inspection, Inspector
from sqlalchemy.orm import object_mapper
from sqlalchemy.orm import session

import logic_engine
from logic_engine.rule_bank.rule_bank import RuleBank
from sqlalchemy.ext.declarative import declarative_base

# from logic_engine.exec_row_logic.parent_role_adjuster import ParentRoleAdjuster
from logic_engine.rule_bank import rule_bank_withdraw
from logic_engine.rule_type.constraint import Constraint
from logic_engine.rule_type.formula import Formula
from logic_engine.rule_type.row_event import EarlyRowEvent


class LogicRow:
    """
    Wraps row, with old_row, ins_upd_dlt, nest_level, session, etc - passed to user logic.
    Methods for insert(), update and delete - called from before_flush listeners, to execute rules
    Helper Methods (get_parent_logic_row(role_name), log, etc)
    """

    def __init__(self, row: base, old_row: base, ins_upd_dlt: str, nest_level: int, a_session: session):
        self.session = a_session
        self.row = row
        self.old_row = old_row
        self.ins_upd_dlt = ins_upd_dlt
        self.nest_level = nest_level

        rb = RuleBank()
        self.rb = rb
        self.session = rb._session
        self.engine = rb._engine
        self.some_base = declarative_base()

        self.name = type(self.row).__name__
        self.table_meta = row.metadata.tables[type(self.row).__name__]
        self.inspector = Inspector.from_engine(self.engine)

    def make_copy(self, a_row: base) -> base:
        result_class = a_row.__class__
        result = result_class()
        row_mapper = object_mapper(a_row)
        for each_attr in row_mapper.attrs:  # TODO skip object references
            setattr(result, each_attr.key, getattr(a_row, each_attr.key))
        return result

    def get_parent_logic_row(self, role_name: str):  # FIXME "-> LogicRow" fails to compile
        parent_row = getattr(self.row, role_name)
        if parent_row is None:
            my_mapper = object_mapper(self.row)
            role_def = my_mapper.relationships.get(role_name)
            if role_def is None:
                raise Exception(f"FIXME invalid role name {role_name}")
            parent_key = {}
            for each_child_col, each_parent_col in role_def.local_remote_pairs:
                parent_key[each_parent_col.name] = getattr(self.row, each_child_col.name)
            parent_class = role_def.entity.class_
            # https://docs.sqlalchemy.org/en/13/orm/query.html#the-query-object
            parent_row = self.session.query(parent_class).get(parent_key)
            setattr(self.row, role_name, parent_row)
        old_parent = self.make_copy(parent_row)
        parent_logic_row = LogicRow(row=parent_row, old_row=old_parent,
                                    a_session=self.session,
                                    nest_level=1+self.nest_level, ins_upd_dlt="*")
        return parent_logic_row

    def is_different_parent(self, role_name: str) -> bool:
        return False # FIXME placeholder, implementation required

    def __str__(self):
        result = ""
        for x in range(self.nest_level):
            result += ".."
        result += self.row.__tablename__ + "["
        my_meta = self.table_meta
        key_cols = my_meta.primary_key.columns.keys()
        is_first = True
        for each_key_col in key_cols:
            if not is_first:
                result += " | "
            is_first = False
            value = getattr(self.row, each_key_col)
            if isinstance(value, str):
                result += value
            else:
                result += str(value)
        result += "]: "
        cols = self.row.__table__.columns
        sorted_cols = sorted(cols, key=lambda col: col.name)
        is_first = True
        for each_col in sorted_cols:
            each_col_name = each_col.name
            if not is_first:
                result += ", "
            is_first = False
            if each_col_name == "Idxx":
                print("Debug Stop here")
            value = getattr(self.row, each_col_name)
            result += each_col_name + ": "
            old_value = value
            if self.old_row is not None:
                old_value = getattr(self.old_row, each_col_name)
            if value != old_value:
                result += ' [' + str(old_value) + '-->] '
            if isinstance(value, str):
                result += value
            else:
                result += str(value)
        result += f'  row@: {str(hex(id(self.row)))}'
        return result  # str(my_dict)

    def log(self, msg: str):
        output = str(self)
        output = output.replace("]:", "] {" + msg + "}", 1)
        logic_engine.logic_logger.debug(output)  # more on this later

    def log_engine(self, msg: str):
        output = str(self)
        output = output.replace("]:", "] {" + msg + "}", 1)
        logic_engine.engine_logger.debug(output)  # more on this later

    def early_row_events(self):
        self.log_engine("early_events")
        early_row_events = rule_bank_withdraw.generic_rules_of_class(EarlyRowEvent)
        for each_row_event in early_row_events:
            each_row_event.execute(self)
        early_row_events = rule_bank_withdraw.rules_of_class(self, EarlyRowEvent)
        for each_row_event in early_row_events:
            each_row_event.execute(self)

    def copy_rules(self):
        copy_rules = rule_bank_withdraw.copy_rules(self)
        for role_name, copy_rules_for_table in copy_rules.items():
            logic_row = self
            if logic_row.ins_upd_dlt == "ins" or logic_row.is_different_parent(role_name):
                self.log("copy_rules for role: " + role_name)
                parent_logic_row = logic_row.get_parent_logic_row(role_name)
                for each_copy_rule in copy_rules_for_table:
                    each_copy_rule.execute(logic_row, parent_logic_row)

    def formula_rules(self):
        self.log_engine("formula_rules")  # TODO (big) execute in dependency order
        formula_rules = rule_bank_withdraw.rules_of_class(self, Formula)
        for each_formula in formula_rules:
            each_formula.execute(self)

    def constraints(self):
        # self.log("constraints")
        constraint_rules = rule_bank_withdraw.rules_of_class(self, Constraint)
        for each_constraint in constraint_rules:
            each_constraint.execute(self)

    def cascade_to_children(self):
        self.log("cascades")

    def adjust_parent_aggregates(self):
        # self.log("adjust_parent_aggregates")
        aggregate_rules = rule_bank_withdraw.aggregate_rules(child_logic_row=self)
        for each_parent_role, each_aggr_list in aggregate_rules.items():
            # print(each_parent_role)
            parent_adjuster = ParentRoleAdjuster(child_logic_row=self,
                                                 parent_role_name=each_parent_role)
            for each_aggregate in each_aggr_list:
                each_aggregate.adjust_parent(parent_adjuster)  # adjusts each_parent iff req'd
            parent_adjuster.save_altered_parents()

    def update(self, reason: str = None):
        self.log("Update - " + reason)
        self.early_row_events()
        self.copy_rules()
        self.formula_rules()
        self.adjust_parent_aggregates()
        self.constraints()
        self.cascade_to_children()

    def insert(self, reason: str = None):
        self.log("Insert - " + reason)
        self.early_row_events()
        self.copy_rules()
        self.formula_rules()
        self.adjust_parent_aggregates()
        self.constraints()
        # self.cascade_to_children()


class ParentRoleAdjuster:
    """
    Passed to <aggregate>.adjust_parent who will set parent row(s) values
    iff adjustment is required (e.g., summed value changes, where changes, fk changes, etc)
    This ensures only 1 update per set of aggregates along a given role
    """

    def __init__(self, parent_role_name: str, child_logic_row: LogicRow):

        self.child_logic_row = child_logic_row  # the child (curr, old values)

        self.parent_role_name = parent_role_name  # which parent are we dealing with?
        self.parent_logic_row = None
        self.previous_parent_logic_row = None

    def save_altered_parents(self):
        if self.parent_logic_row is None:  # save *only altered* parents (often does nothing)
            pass
            # self.child_logic_row.log("adjust not required for parent_logic_row: " + str(self))
        else:
            # self.child_logic_row.log("adjust required for parent_logic_row: " + str(self))
            current_session = self.child_logic_row.session
            self.parent_logic_row.ins_upd_dlt = "upd"
            current_session.add(self.parent_logic_row.row)
            self.parent_logic_row.update(reason="Adjusting " + self.parent_role_name)

        if self.previous_parent_logic_row is None:
            pass
            # self.child_logic_row.log("save-adjusted not required for previous_parent_logic_row: " + str(self))
        else:
            raise Exception("Not Implemented - adjust required for previous_parent_logic_row: " + str(self))
