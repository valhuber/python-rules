from sqlalchemy.orm import session

import logic_engine
from logic_engine.exec_row_logic.logic_row import LogicRow
from logic_engine.exec_trans_logic.row_sets import RowSets
from logic_engine.rule_bank import rule_bank_withdraw
from logic_engine.rule_type.row_event import CommitRowEvent
from logic_engine.util import get_old_row, prt


def before_commit(a_session: session):
    """
    Unused
        * not called for auto-commit transactions
        * called prior to before_flush
    """
    logic_engine.logic_logger.debug("\nBefore Commit Phase          \t\t\t\t\t")


def before_flush(a_session: session, a_flush_context, an_instances):
    """
    Logic Execution processes LogicRows: row and old_row

    Note old_row is critical for:
        * user logic (did the value change?  by how much?)
        * performance / pruning (skip rules iff no dependent values change)
        * performance / optimization (1 row adjustments, not expensive select sum/count)
    """

    """
    Logic Phase
    """
    logic_engine.logic_logger.debug("Logic Phase (sqlalchemy before_flush)\t\t\t")
    # print("\n***************** sqlalchemy calls logic_engine\n")

    row_sets = RowSets()  # type : RowSet
    for each_instance in a_session.dirty:
        row_sets.add_submitted(each_instance)

    bug_explore = None  # [None, None]
    if bug_explore is not None:  # temp hack - order rows to explore bug (upd_order_reuse)
        temp_debug(a_session, bug_explore, row_sets)
    else:
        for each_instance in a_session.dirty:
            table_name = each_instance.__tablename__
            old_row = get_old_row(each_instance)
            logic_row = LogicRow(row=each_instance, old_row=old_row, ins_upd_dlt="upd",
                                 nest_level=0, a_session=a_session, row_sets=row_sets)
            logic_row.update(reason="client")

    for each_instance in a_session.new:
        table_name = each_instance.__tablename__
        logic_row = LogicRow(row=each_instance, old_row=None, ins_upd_dlt="ins",
                             nest_level=0, a_session=a_session, row_sets=row_sets)
        logic_row.insert(reason="client")

    """
    Commit Logic Phase
    """
    logic_engine.logic_logger.debug("Commit Logic Phase   \t\t\t")
    for each_logic_row_key in row_sets.processed_rows:
        each_logic_row = row_sets.processed_rows[each_logic_row_key]
        logic_engine.engine_logger.debug("visit: " + each_logic_row.__str__())
        commit_row_events = rule_bank_withdraw.rules_of_class(each_logic_row, CommitRowEvent)
        for each_row_event in commit_row_events:
            each_logic_row.log("Commit Event")
            each_row_event.execute(each_logic_row)

    """
    Proceed with sqlalchemy flush processing
    """
    logic_engine.logic_logger.debug("Flush Phase          \t\t\t")


def temp_debug(a_session, bug_explore, row_cache):
    """
    see description in nw/trans_tests/upd_order_reuse
    """
    for each_instance in a_session.dirty:
        table_name = each_instance.__tablename__
        if table_name.startswith("OrderDetail"):
            bug_explore[0] = each_instance
        else:
            bug_explore[1] = each_instance
    each_instance = bug_explore[0]
    old_row = get_old_row(each_instance)
    logic_row = LogicRow(row=each_instance, old_row=old_row, ins_upd_dlt="upd",
                         nest_level=0, a_session=a_session, row_sets=row_cache)
    logic_row.update(reason="client")
    each_instance = bug_explore[1]
    old_row = get_old_row(each_instance)
    logic_row = LogicRow(row=each_instance, old_row=old_row, ins_upd_dlt="upd",
                         nest_level=0, a_session=a_session, row_sets=row_cache)
    logic_row.update(reason="client")

