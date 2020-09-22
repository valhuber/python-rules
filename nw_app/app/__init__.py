import logging
import os
import sys

from flask import Flask
from flask_appbuilder import AppBuilder, SQLA

use_rules = True

if use_rules:
    cwd = os.getcwd()  # eg, /Users/val/python/pycharm/python-rules/nw_app
    required_path_python_rules = cwd  # seeking /Users/val/python/pycharm/python-rules
    required_path_python_rules = required_path_python_rules.replace("/nw_app", "")

    sys_path = ""
    required_path_present = False
    for each_node in sys.path:
        sys_path += each_node + "\n"
        if each_node == required_path_python_rules:
            required_path_present = True
    print("\n sys.path...\n" + sys_path)
    if not required_path_present:
        print("Fixing path (so can run from terminal) with: " +
              required_path_python_rules)
        sys.path.append(required_path_python_rules)
    else:
        pass
        print("NOT Fixing path (default PyCharm, set in VSC Launch Config): " +
              required_path_python_rules)

    import nw.nw_logic.models as models
    from logic_engine.util import row_prt, prt
    from nw.nw_logic import session  # opens db, activates logic listener <--

    """
    fails: circular imports
        withdraw -> logic_row -> rule_bank -> util -> nw_logic/init -> rule_bank_setup -> RuleBank
    """
    from logic_engine.rule_bank import rule_bank_withdraw  # FIXME design why required to avoid circular imports??
    from logic_engine.rule_bank import rule_bank_setup
    from nw.nw_logic import activate_basic_check_credit_rules

"""
 Logging configuration
"""

logging.basicConfig(format="%(asctime)s:%(levelname)s:%(name)s:%(message)s")
logging.getLogger().setLevel(logging.DEBUG)

app = Flask(__name__)
app.config.from_object("config")
db = SQLA(app)

appbuilder = AppBuilder(app, db.session)

if use_rules:
    rule_bank_setup.setup(db.session, db.engine)
    activate_basic_check_credit_rules()
    rule_bank_setup.validate(db.session, db.engine)  # checks for cycles, etc

"""
from sqlalchemy.engine import Engine
from sqlalchemy import event

#Only include this for SQLLite constraints
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    # Will force sqllite contraint foreign keys
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()
"""

from . import views
