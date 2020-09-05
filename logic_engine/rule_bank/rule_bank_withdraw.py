from typing import TypedDict, List

import sqlalchemy
from sqlalchemy.orm import object_mapper

from logic_engine.exec_row_logic.logic_row import LogicRow
from logic_engine.rule_bank.rule_bank import RuleBank
from logic_engine.rule_type.constraint import Constraint
from logic_engine.rule_type.copy import Copy
from logic_engine.rule_type.count import Count
from logic_engine.rule_type.formula import Formula
from logic_engine.rule_type.sum import Sum

"""
There really want to be instance methods on RuleBank, but circular imports...
"""


class RoleRules:
    """returns list of rules grouped by role, so logic can access related row only once
    (not once per rule)
    """

    def __init__(self):
        self._role_name = ""
        self._role_rules = []  # list of rule objects


class CopyRulesForTable(TypedDict):
    copy_rules: List[Copy]
    label: str


def copy_rules(logic_row: LogicRow) -> CopyRulesForTable:
    """dict(<role_name>, copy_rules[]
    """
    rule_bank = RuleBank()
    role_rules_list = {}  # dict of RoleRules
    for each_rule in rule_bank._tables[logic_row.name]:
        if isinstance(each_rule, Copy):
            role_name = each_rule._from_parent_role
            if role_name not in role_rules_list:
                role_rules_list[role_name] = []
            role_rules_list[role_name].append(each_rule)
    return role_rules_list

"""
Rule Bank is a dict of <table><rule-list>, e.g.:

Table[Customer] rules:
  Constraint Function: None 
  Derive Customer.balance as Sum(OrderList.AmountTotal Where ShippedDate not None)
  Derive Customer.OrderCount as Count(Order Where ShippedDate not None)
Table[Order] rules:
  Derive Order.AmountTotal as Sum(OrderDetail.Amount Where None)
Table[OrderDetail] rules:
  Derive OrderDetail.Amount as Formula Function: None 
  Derive OrderDetail.UnitPrice as Copy(Product.UnitPrice)
"""


def aggregate_rules(child_logic_row: LogicRow) -> dict:
    """returns dict(<role_name>, sum/count_rules[] for given child_table_name
    This requires we **invert** the RuleBank, to find sums that reference child_table_name
    e.g., for child_table_name "Order", we return the Customer.balance rule
    """
    result_role_rules_list = {}  # dict of RoleRules

    child_mapper = object_mapper(child_logic_row.row)
    rule_bank = RuleBank()
    relationships = child_mapper.relationships
    for each_relationship in relationships:  # eg, order has parents cust & emp, child orderdetail
        if each_relationship.direction == sqlalchemy.orm.interfaces.MANYTOONE:  # cust, emp
            child_role_name = each_relationship.back_populates  # eg, OrderList
            if child_role_name is None:
                child_role_name = child_mapper.class_.__name__  # default TODO review
            parent_role_name = each_relationship.key   # eg, Customer TODO review
            parent_class_name = each_relationship.entity.class_.__name__
            if parent_class_name in rule_bank._tables:
                parent_rules = rule_bank._tables[parent_class_name]
                for each_parent_rule in parent_rules:  # (..  bal = sum(OrderList.amount) )
                    if isinstance(each_parent_rule, (Sum, Count)):
                        if each_parent_rule._child_role_name == child_role_name:
                            if parent_role_name not in result_role_rules_list:
                                result_role_rules_list[parent_role_name] = []
                            result_role_rules_list[parent_role_name].append(each_parent_rule)
    return result_role_rules_list


"""    rule_bank = RuleBank()
    for each_rule in rule_bank._tables[child_table_name]:
        if isinstance(each_rule, (Sum, Count)):
            role_name = each_rule._from_parent_role
            if role_name not in role_rules_list:
                role_rules_list[role_name] = []
            role_rules_list[role_name].append(each_rule)
"""


def rules_of_class(logic_row: LogicRow, a_class: (Formula, Constraint)) -> list:
    """withdraw rules of designated a_class
    """
    rule_bank = RuleBank()
    rules_list = []
    role_rules_list = {}  # dict of RoleRules
    for each_rule in rule_bank._tables[logic_row.name]:
        if isinstance(each_rule, a_class):
            rules_list.append(each_rule)
    return rules_list
