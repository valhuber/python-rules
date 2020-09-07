import os

import sqlalchemy
from sqlalchemy import event
from sqlalchemy.orm import session

from logic_engine.rule_bank.rule_bank import RuleBank
from logic_engine.rule_bank import rule_bank_withdraw
from logic_engine.rule_bank import rule_bank_setup
from logic_engine.rule_type.constraint import Constraint
from logic_engine.rule_type.formula import Formula
from nw.nw_logic.order_code import order_commit_dirty, order_flush_dirty, order_flush_new
from nw.nw_logic.order_detail_code import order_detail_flush_new

from nw.nw_logic.models import Order

'''
from nw.nw_logic.listeners import nw_before_commit, nw_before_flush
from nw.nw_logic.order_code import order_modified
'''


def nw_before_commit(a_session: session):
    print("logic: before commit!")
    # for obj in versioned_objects(a_session.dirty):
    for obj in a_session.dirty:
        print("logic: before commit! --> " + str(obj))
        obj_class = obj.__tablename__
        if obj_class == "Order":
            order_commit_dirty(obj, a_session)
        elif obj_class == "OrderDetail":
            print("Stub")
    print("logic called: before commit!  EXIT")


def nw_before_flush(a_session: session, a_flush_context, an_instances):
    print("nw_before_flush")
    for each_instance in a_session.dirty:
        print("nw_before_flush flushing Dirty! --> " + str(each_instance))
        obj_class = each_instance.__tablename__
        if obj_class == "Order":
            order_flush_dirty(each_instance, a_session)
        elif obj_class == "OrderDetail":
            print("Stub")

    for each_instance in a_session.new:
        print("nw_before_flush flushing New! --> " + str(each_instance))
        obj_class = each_instance.__tablename__
        if obj_class == "OrderDetail":
            order_detail_flush_new(each_instance, a_session)
        elif obj_class == "Order":
            order_flush_new(each_instance, a_session)

    print("nw_before_flush  EXIT")


basedir = os.path.abspath(os.path.dirname(__file__))
basedir = os.path.dirname(basedir)
basedir = os.path.dirname(basedir)
conn_string = "sqlite:///" + os.path.join(basedir, "nw-app/nw.db")
# e.g. 'sqlite:////Users/val/python/vsc/logic-explore/nw-app/nw.db'
engine = sqlalchemy.create_engine(conn_string, echo=False)  # sqlalchemy sqls...


# Create a session
session_maker = sqlalchemy.orm.sessionmaker()
session_maker.configure(bind=engine)
session = session_maker()

do_logic = True  # True => rules, False => code
rule_list = None
db = None
if do_logic:
    rule_bank = RuleBank()
    rule_bank_setup.setup(session, engine)
    from nw.nw_logic import nw_rules_bank
    rule_bank = RuleBank()  # FIXME - unclear why this returns the *correct* singleton, vs 2 lines above
    print("\n\nlogic loaded:\n" + str(rule_bank))
else:
    # target, modifier, function
    event.listen(session, "before_commit", nw_before_commit)
    event.listen(session, "before_flush", nw_before_flush)

# event.listen(Order.ShippedDate, "set", order_modified)
print("session created, listeners registered")


'''
@event.listens_for(models.Order.ShippedDate, 'modified')
def receive_modified(target, initiator):
    print('Order Modified (Decorator - __init__')
'''

'''
@event.listens_for(Order, 'before_update')
def before_update(mapper, connection, target):
    state = db.inspect(target)
    changes = {}

    for attr in state.attrs:
        hist = attr.load_history()

        if not hist.has_changes():
            continue

        # hist.deleted holds old value
        # hist.added holds new value
        changes[attr.key] = hist.added

    # now changes map keys to new values
    print ("before update")
'''
