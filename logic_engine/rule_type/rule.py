import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import object_mapper

# from logic_engine.logic import Base  # circular import
# from logic_engine.rule_bank.rule_bank import RuleBank # circular import


class Rule(object):
    table = None  # FIXME remove

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
        parent_mapper = object_mapper(child_class)  # , eg, Order propagates ShippedDate => OrderDetailList
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
        Base = declarative_base()
        # Base = logic.Base
        metadata = Base.metadata  # FIXME this should prolly be class
        Base = RuleBank()._rb_base
        for c in Base._decl_class_registry.values():
            if hasattr(c, '__tablename__') and c.__tablename__ == tablename:
                return c