from __future__ import annotations
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import object_mapper

from logic_engine import engine_logger
from logic_engine.rule_bank import rule_bank_withdraw
from sqlalchemy.orm import mapperlib

# Circular imports prevent these (geesh ** 2):
# https://stackoverflow.com/questions/33837918/type-hints-solve-circular-dependency
from logic_engine.rule_bank.rule_bank import RuleBank, TableRules  # circular import
# from logic_engine.logic import Base  # circular import
# from logic_engine.rule_bank import rule_bank_setup
# from logic_engine.rule_type import log_dependency
from logic_engine.util import prt


class Rule(object):

    def __init__(self, a_table_name: str):
        #  failed -- mapped_class = get_class_by_table(declarative_base(), a_table_name)  # User class
        self.table = a_table_name  # FIXME wrong, should be class not table
        self._dependencies = ()

    def parse_dependencies(self, rule_text: str):
        """
        Split rule_text into space-separated words
        Set <rule>._dependencies() to all words starting with "row."
        """
        words = rule_text.split()
        for each_word in words:
            if each_word.startswith("row."):  # allow Cust.CreditLimit?
                dependencies = each_word.split('.')
                if len(dependencies) == 2:
                    self._dependencies.append(dependencies[1])
                else:
                    self._dependencies.append(dependencies[1] +
                                              "." + dependencies[2])
                    self.update_referenced_parent_attributes(dependencies)

    def update_referenced_parent_attributes(self, dependencies: list):
        """
        Used by Formulas and constraints log their dependence on parent attributes
        This sets RuleBank.TableRules[mapped_class].referring_children
        dependencies is a list

        But, can't do this now, because meta_contains_role_name = False
        So, do it on the fly in logic_row (which is an ugh)
        """
        meta_contains_role_name = False
        if meta_contains_role_name is False:
            return
        else:
            meta_data = rule_bank_withdraw.get_meta_data()
            child_meta = meta_data.tables[self.table]
            parent_role_name = dependencies[1]
            foreign_keys = child_meta.foreign_keys
            for each_foreign_key in foreign_keys:  # eg, OrderDetail has OrderHeader, Product
                each_parent_class_name = each_foreign_key.name
                each_parent_role_name = each_foreign_key.key
                if parent_role_name == each_parent_role_name:  # eg, OrderHeader
                    rule_bank = RuleBank()
                    if each_parent_class_name not in rule_bank._tables:
                        self._tables[rule_bank] = TableRules()
                    table_rules = self._tables[rule_bank]
                    if table_rules.referring_children is None:
                        table_rules.referring_children = {}
                    if parent_role_name not in table_rules.referring_children:
                        table_rules.referring_children[parent_role_name] = []
                    table_rules.referring_children.append(dependencies[2])
                    engine_logger.debug(prt("child parent dependency: " + dependencies[1]))
                    break

    def get_class_by_tablename(self, tablename):
        """Return class reference mapped to table.

        :param tablename: String with name of table.
        :return: Class reference or None.
        https://stackoverflow.com/questions/11668355/sqlalchemy-get-model-from-table-name-this-may-imply-appending-some-function-to
        FIXME - unable to get working (remove)
        """
        use_table_name = True  # FIXME - should be using class name
        if use_table_name:
            meta_data = rule_bank_withdraw.get_meta_data()
            result = meta_data.tables[tablename]
            return result
        else:
            meta_data = rule_bank_withdraw.get_meta_data()
            session = rule_bank_withdraw.get_session()
            from sqlalchemy.ext.declarative import declarative_base
            Base = declarative_base()
            for c in Base._decl_class_registry.values():
                if hasattr(c, '__tablename__') and c.__tablename__ == tablename:
                    return c

    def find_table_mapper(self, tbl):
        """
        https://stackoverflow.com/questions/51529759/sqlalchemy-get-mapper-object-from-table-object-from-metadata-or-session-or-othe
        FIXME - unable to get working (remove)
        """
        mappers = [
            mapper for mapper in mapperlib._mapper_registry
            if tbl in mapper.tables
        ]
        if len(mappers) > 1:
            raise ValueError(
                "Multiple mappers found for table '%s'." % tbl.name
            )
        elif not mappers:
            raise ValueError(
                "Could not get mapper for table '%s'." % tbl.name  # fails here
            )
        else:
            return mappers[0]