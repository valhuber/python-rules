import sqlalchemy
import sqlalchemy_utils
from sqlalchemy.ext.declarative import base
from sqlalchemy.engine.reflection import inspection, Inspector
from sqlalchemy.orm import object_mapper
from sqlalchemy.orm import session

from logic_engine.rule_bank.rule_bank import RuleBank
from sqlalchemy.ext.declarative import declarative_base


class LogicRow:
    """
    Wraps row, with mold_row, ins_upd_dlt, nest_level, etc
    State for row logic execution
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
        old_parent = self.make_copy(parent_row)
        parent_logic_row = LogicRow(row=parent_row, old_row=old_parent,
                                    a_session=self.session,
                                    nest_level=1+self.nest_level, ins_upd_dlt="*")
        return parent_logic_row

    def is_different_parent(self, role_name: str) -> bool:
        return False # FIXME placeholder, implementation required

    def __str__(self):
        result = self.row.__tablename__ + "["
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
        result += "] "
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
                result += ' [' + str(old_value) + '-->]'
            if isinstance(value, str):
                result += value
            else:
                result += str(value)
        return result  # str(my_dict)
