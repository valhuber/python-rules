import logging
import os
import sys

from flask import Flask
from flask_appbuilder import AppBuilder, SQLA

use_rules = True

if use_rules:
    cwd = os.getcwd()
    required_path_python_rules = cwd
    required_path_python_rules = required_path_python_rules.replace("/banking-app", "")

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

    import banking.banking_logic.models as models
    from python_rules.util import row_prt, prt
    from banking.banking_logic import session  # opens db, activates logic listener <--

    from python_rules.rule_bank import rule_bank_withdraw  # required to avoid circular imports
    from python_rules.rule_bank import rule_bank_setup
    from banking.banking_logic.banking_rules_bank import activate_basic_rules

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
    activate_basic_rules()
    rule_bank_setup.validate(db.session, db.engine)  # checks for cycles, etc



from . import views
