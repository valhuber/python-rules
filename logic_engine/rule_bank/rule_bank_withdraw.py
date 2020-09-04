from typing import TypedDict, List

from logic_engine.rule_bank.rule_bank import RuleBank
from logic_engine.rule_type.constraint import Constraint
from logic_engine.rule_type.copy import Copy
from logic_engine.rule_type.count import Count
from logic_engine.rule_type.formula import Formula
from logic_engine.rule_type.sum import Sum


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


def copy_rules(a_table_name: str) -> CopyRulesForTable:
    """dict(<role_name>, copy_rules[]
    """
    rule_bank = RuleBank()
    role_rules_list = {}  # dict of RoleRules
    for each_rule in rule_bank._tables[a_table_name]:
        if isinstance(each_rule, Copy):
            role_name = each_rule._from_parent_role
            if role_name not in role_rules_list:
                role_rules_list[role_name] = []
            role_rules_list[role_name].append(each_rule)
    return role_rules_list


def aggregate_rules(a_table_name: str) -> dict:
    """dict(<role_name>, sum/count_rules[]
    """
    rule_bank = RuleBank()
    role_rules_list = {}  # dict of RoleRules
    for each_rule in rule_bank._tables[a_table_name]:
        if isinstance(each_rule, (Sum, Count)):
            role_name = each_rule._from_parent_role
            if role_name not in role_rules_list:
                role_rules_list[role_name] = []
            role_rules_list[role_name].append(each_rule)
    return role_rules_list


def rules_of_class(a_table_name: str, a_class: (Formula, Constraint)) -> list:
    """withdraw rules of designated a_class
    """
    rule_bank = RuleBank()
    rules_list = []
    role_rules_list = {}  # dict of RoleRules
    for each_rule in rule_bank._tables[a_table_name]:
        if isinstance(each_rule, a_class):
            rules_list.append(each_rule)
    return rules_list
