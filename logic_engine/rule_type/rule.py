import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import object_mapper

# from logic_engine.logic import Base  # circular import
from logic_engine.rule_bank import rule_bank_withdraw
# from logic_engine.rule_bank.rule_bank import RuleBank # circular import
from sqlalchemy.orm import mapperlib


class Rule(object):

    def __init__(self, a_table_name: str):
        #  failed -- mapped_class = get_class_by_table(declarative_base(), a_table_name)  # User class
        self.table = a_table_name
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
                    # self.update_referenced_parent_attributes(dependencies)

    def update_referenced_parent_attributes(self, dependencies: list):
        """
        Used by Formulas and constraints log their dependence on parent attributes
        This sets RuleBank.TableRules[mapped_class].referring_children
        dependencies is a list
        """
        child_class = self.get_class_by_tablename(self.table)
        parent_mapper = get_mapper(local_table=child_class)
        parent_mapper = self.find_table_mapper(child_class)  # , eg, Order propagates ShippedDate => OrderDetailList
        relationships = parent_mapper.relationships
        for each_relationship in relationships:  # eg, order has parents cust & emp, child orderdetail
            if each_relationship.direction == sqlalchemy.orm.interfaces.ONETOMANY:  # orderdetail
                child_role_name = each_relationship.back_populates  # eg,
                if child_role_name is None:
                    child_role_name = parent_mapper.class_.__name__  # default TODO review
                parent_role_name = each_relationship.key  # eg, Customer TODO review
                parent_class_name = each_relationship.entity.class_.__name__

    def get_class_by_tablename(self, tablename):
        """Return class reference mapped to table.

        :param tablename: String with name of table.
        :return: Class reference or None.
        https://stackoverflow.com/questions/11668355/sqlalchemy-get-model-from-table-name-this-may-imply-appending-some-function-to
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