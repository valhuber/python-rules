from sqlalchemy import event

import nw.nw_logic.models as models
from sqlalchemy.orm import session

from logic_engine.util import get_old_row, row_prt, row2dict, ObjectView


# https://docs.sqlalchemy.org/en/13/_modules/examples/versioned_history/history_meta.html
from nw.nw_logic.customer_code import customer_update


def order_flush_dirty(a_row, a_session: session):
    """
    Called from listeners.py on before_flush
    E.g., altering an Order ShippedDate (we must adjust Customer balance)
    """
    old_row = get_old_row(a_row)
    order_update(a_row, old_row, a_session)


def order_update(a_row, an_old_row, a_session):
    """
    called either by order_flush_dirty, *or* by order_detail_code. to adjust order
    see order_detail_code.order_detail_flush_new
    """
    row_prt(a_row, "\norder_flush_dirty")

    if a_row.ShippedDate != an_old_row.ShippedDate:
        is_unshipped = (a_row.ShippedDate is None) or (a_row.ShippedDate == "")
        delta = - a_row.AmountTotal  # assume not changed!!
        if is_unshipped:
            delta = a_row.AmountTotal
        customer = a_row.Customer
        customer.Balance += delta  # attach, update not req'd
        row_prt(customer, "order_upd adjusted per shipped change")

    if a_row.CustomerId != an_old_row.CustomerId:
        raise Exception("\norder_upd/ change Cust not implemented")

    if a_row.AmountTotal != an_old_row.AmountTotal:
        # nice try customer = a_row.Customer
        customer = a_session.query(models.Customer). \
            filter(models.Customer.Id == a_row.CustomerId).one()
        old_customer = ObjectView(row2dict(customer))
        delta = a_row.AmountTotal - an_old_row.AmountTotal
        customer.Balance += delta  # attach, update not req'd
        a_session.add(customer)
        customer_update(customer, old_customer, a_session)
        row_prt(customer, "order_upd adjusted Customer, per AmountTotal change")


def order_flush_new(a_row, a_session: session):
    """
    Called from listeners.py on before_flush
    """
    a_row.ShippedDate = ""  # default value
    row_prt(a_row, "order_flush_new - default values supplied")


# happens before flush
def order_commit_dirty(a_row, a_session: session):
    old_row = get_old_row(a_row)
    row_prt(a_row, "order_commit_dirty")


# *********************** unused experiments *************************

def order_modified(object):
    print("order_modified - experiment with this (failed, not used)")

@event.listens_for(models.Order.ShippedDate, 'modified')
def receive_modified(target, initiator):
    print("receive_modified - experiment with this (failed, not used)")

'''
    # standard decorator style
    @event.listens_for(SomeClass.some_attribute, 'set')
    def receive_set(target, value, oldvalue, initiator):
        "listen for the 'set' event"

        # ... (event handling logic) ...
    @event.listens_for(SomeClass.some_attribute, 'modified')
    def receive_modified(target, initiator):
        "listen for the 'modified' event"
'''