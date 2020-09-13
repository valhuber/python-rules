from logic_engine import engine_logger
from logic_engine.util import prt
from logic_engine.rule_type.rule import Rule
from datetime import datetime

# https://stackoverflow.com/questions/6760685/creating-a-singleton-in-python


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class TableRules(object):

    def __init__(self):
        self.rules = []
        self.child_references = {}


class RuleBank(metaclass=Singleton):
    """
    scans for rules, creates the logic_repository
    """

    _tables = {}  # key = mapped class name, value = list of TableRules
    _rb_base = None
    _at = datetime.now()
    _session = None
    _engine = None

    def __init__(self):
        pass

    def deposit_rule(self, a_rule: Rule):
        if a_rule.table not in self._tables:
            self._tables[a_rule.table] = TableRules()
        table_rules = self._tables[a_rule.table]
        table_rules.rules.append(a_rule)
        engine_logger.debug(prt(str(a_rule)))

    def __str__(self):
        result = f"Rule Bank[{str(hex(id(self)))}] (loaded {self._at})"
        for each_key in self._tables:
            result += f"\nMapped Class[{each_key}] rules:"
            table_rules = self._tables[each_key]
            for each_rule in table_rules.rules:
                result += f'\n  {str(each_rule)}'
        return result


