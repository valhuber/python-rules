from sqlalchemy.orm import session

from logic_engine.exec_row_logic.logic_row import LogicRow
from logic_engine.exec_row_logic.row_logic_exec import RowLogicExec


def before_flush(a_session: session, a_flush_context, an_instances):
    print("logic.logic_exec.listeners>before_flush BEGIN")
    for each_instance in a_session.dirty:
        table_name = each_instance.__tablename__
        print("logic.logic_exec.listeners>before_flush flushing Dirty! "
              + str(table_name) + "]--> " + str(each_instance))

    for each_instance in a_session.new:
        table_name = each_instance.__tablename__
        print("logic.logic_exec.listeners>before_flush flushing New! "
              + str(table_name) + "]--> " + str(each_instance))
        logic_row = LogicRow(row=each_instance, old_row=None, nest_level=0, ins_upd_dlt="ins")
        row_logic_exec = RowLogicExec(logic_row=logic_row)
        row_logic_exec.insert()

    # print("logic.logic_exec.listeners>before_flush  RuleBank: " + rb.__str__())
    print("logic.logic_exec.listeners>before_flush  END")
