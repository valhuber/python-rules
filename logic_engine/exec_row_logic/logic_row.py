import sqlalchemy
import sqlalchemy_utils
from sqlalchemy.ext.declarative import base
from sqlalchemy.engine.reflection import inspection, Inspector
from sqlalchemy.orm import object_mapper, session, relationships

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
        self.ins_upd_dlt_initial = ins_upd_dlt  # order inserted, then adjusted
        self.nest_level = nest_level

        rb = RuleBank()
        self.rb = rb
        self.session = rb._session
        self.engine = rb._engine
        self.some_base = declarative_base()

        self.name = type(self.row).__name__
        self.table_meta = row.metadata.tables[type(self.row).__name__]
        self.inspector = Inspector.from_engine(self.engine)

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
        logic_engine.engine_logger.debug(output)

    def make_copy(self, a_row: base) -> base:
        result_class = a_row.__class__
        result = result_class()
        row_mapper = object_mapper(a_row)
        for each_attr in row_mapper.columns:  # TODO skip object references
            setattr(result, each_attr.key, getattr(a_row, each_attr.key))
        return result

    def get_parent_logic_row(self, role_name: str, for_update: bool = False):  # FIXME "-> LogicRow" fails to compile
        parent_row = getattr(self.row, role_name)
        always_reread_parent = True  # FIXME design - else FlushError("New instance... conflicts
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
            if self.ins_upd_dlt == "upd":  # eg, add order - don't tell sqlalchemy to add cust
                pass
                # setattr(self.row, role_name, parent_row)
            if for_update:
                self.session.expunge(parent_row)
        old_parent = self.make_copy(parent_row)
        parent_logic_row = LogicRow(row=parent_row, old_row=old_parent,
                                    a_session=self.session,
                                    nest_level=1+self.nest_level, ins_upd_dlt="*")
        return parent_logic_row

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
                for each_copy_rule in copy_rules_for_table:  # TODO consider orphans
                    each_copy_rule.execute(logic_row, parent_logic_row)

    def is_different_parent(self, role_name: str) -> bool:
        my_mapper = object_mapper(self.row)
        role_def = my_mapper.relationships.get(role_name)
        if role_def is None:
            raise Exception(f"FIXME invalid role name {role_name}")
        row = self.row
        for each_child_col, each_parent_col in role_def.local_remote_pairs:
            each_child_col_name = each_child_col.key
            if getattr(row, each_child_col_name) != getattr(row, each_child_col_name):
                return True
        return False

    def is_formula_pruned(self, formula: Formula) -> bool:
        """
        Prune Conservatively:
         * if delete, or
         * has parent refs & no dependencies changed (skip parent read)
        e.g. always execute formulas with no dependencies
        """
        result_prune = True
        row = self.row
        old_row = self.old_row
        if self.ins_upd_dlt == "ins":
            result_prune = False
        elif self.ins_upd_dlt == "dlt":
            result_prune = True
        else:
            is_parent_changed = False
            is_dependent_changed = False
            for each_dependency in formula._dependencies:
                column = each_dependency
                if column.contains('.'):
                    role_name = column.split(".")[1]
                    if self.is_different_parent(role_name):
                        is_parent_changed = True
                        break
                else:
                    if getattr(row, column) == getattr(old_row, column):
                        is_dependent_changed = True
                        break
            result_prune = is_parent_changed or is_dependent_changed
        if result_prune:
            self.log_engine("Prune Formula: " + formula._column)
        return result_prune


    def formula_rules(self):
        self.log_engine("formula_rules")
        formula_rules = rule_bank_withdraw.rules_of_class(self, Formula)
        formula_rules.sort(key=lambda f: f._exec_order)
        for each_formula in formula_rules:
            if not self.is_formula_pruned(each_formula):
                each_formula.execute(self)
        """
        FIXME design nasty issue
        get_parent_logic_row cannot fill the reference
        so, how does it reference the parent consistently?
        eg. Component.Product.Price
        fill it, then Null it?? (good grief)
        """

    def constraints(self):
        # self.log("constraints")
        constraint_rules = rule_bank_withdraw.rules_of_class(self, Constraint)
        for each_constraint in constraint_rules:
            each_constraint.execute(self)

    def cascade_to_children(self):
        pass

    def load_parents(self):
        """ sqlalchemy lazy does not work for inserts, do it here
        1. RI would require the sql anyway
        2. Provide a consistent model - your parents are always there for you

        FIXME fails flush error identity key, disabled
        """
        def is_foreign_key_null(relationship: sqlalchemy.orm.relationships):
            child_columns = relationship.local_columns
            for each_child_column in child_columns:
                each_child_column_name = each_child_column.name
                if getattr(self.row, each_child_column_name) is None:
                    return True
            return False

        child_mapper = object_mapper(self.row)
        my_relationships = child_mapper.relationships
        for each_relationship in my_relationships:  # eg, order has parents cust & emp, child orderdetail
            if each_relationship.direction == sqlalchemy.orm.interfaces.MANYTOONE:  # cust, emp
                parent_role_name = each_relationship.key  # eg, OrderList
                if is_foreign_key_null(each_relationship) is False:
                    continue#
                    #  self.get_parent_logic_row(parent_role_name)  # see comment above
        return self

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
        self.load_parents()
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
            #  current_session.add(self.parent_logic_row.row)  -- read ==> attached
            self.parent_logic_row.update(reason="Adjusting " + self.parent_role_name)
            # no after_flush: https://stackoverflow.com/questions/63563680/sqlalchemy-changes-in-before-flush-not-triggering-before-flush
        if self.previous_parent_logic_row is None:
            pass
            # self.child_logic_row.log("save-adjusted not required for previous_parent_logic_row: " + str(self))
        else:
            raise Exception("Not Implemented - adjust required for previous_parent_logic_row: " + str(self))
