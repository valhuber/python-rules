from sqlalchemy.orm import session

import logic_engine
from logic_engine.exec_row_logic.logic_row import LogicRow
from logic_engine.util import get_old_row, prt


def before_flush(a_session: session, a_flush_context, an_instances):
    """
    Logic Execution processes LogicRows: row and old_row

    Note old_row is critical for:
        * user logic (did the value change?  by how much?)
        * performance / pruning (skip rules iff no dependent values change)
        * performance / optimization (1 row adjustments, not expensive select sum/count)
    """
    logic_engine.logic_logger.debug("\nlogic.logic_exec.listeners>before_flush: --> TRANSACTION LOGIC BEGIN\t\t\t")
    for each_instance in a_session.dirty:
        table_name = each_instance.__tablename__
        old_row = get_old_row(each_instance)
        logic_row = LogicRow(row=each_instance, old_row=old_row, nest_level=0, ins_upd_dlt="upd", a_session=a_session)
        logic_row.update(reason="client")

    for each_instance in a_session.new:
        table_name = each_instance.__tablename__
        logic_row = LogicRow(row=each_instance, old_row=None, nest_level=0, ins_upd_dlt="ins", a_session=a_session)
        logic_row.insert(reason="client")

    logic_engine.logic_logger.debug("logic.logic_exec.listeners>before_flush: --> TRANSACTION LOGIC END   \t\t\t")
