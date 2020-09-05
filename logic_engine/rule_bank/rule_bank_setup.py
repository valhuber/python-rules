from datetime import datetime

from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base

from logic_engine.exec_trans_logic.listeners import before_flush
from logic_engine.rule_bank.rule_bank import RuleBank
from nw.nw_logic import session


def setup(a_session: session, an_engine: Engine):
    rules_bank = RuleBank()
    rules_bank._session = a_session
    event.listen(a_session, "before_flush", before_flush)
    rules_bank._tables = {}
    rules_bank._at = datetime.now()

    rules_bank._engine = an_engine
    rules_bank._rb_base = declarative_base  # FIXME good grief, not appearing, no error
    return


def validate(a_session: session, engine: Engine):
    rules_bank = RuleBank()

