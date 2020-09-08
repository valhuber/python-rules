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


class RuleBank(metaclass=Singleton):
    """
    scans for rules, creates the logic_repository
    """

    _tables = {}  # key = tbl_name, value = list of rules
    _rb_base = None
    _at = datetime.now()
    _session = None
    _engine = None

    def __init__(self):
        pass

    def deposit_rule(self, a_rule: Rule):
        if a_rule.table not in self._tables:
            self._tables[a_rule.table] = []
        self._tables[a_rule.table].append(a_rule)
        engine_logger.debug(prt(str(a_rule)))

    def __str__(self):
        result = f"Rule Bank[{str(hex(id(self)))}] (loaded {self._at})"
        for each_key in self._tables:
            result += f"\nMapped Class[{each_key}] rules:"
            for each_rule in self._tables[each_key]:
                result += f'\n  {str(each_rule)}'
        return result


