from sqlalchemy.orm import session

from logic_engine.exec_row_logic.logic_row import LogicRow


def before_flush(a_session: session, a_flush_context, an_instances):
    print("logic.logic_exec.listeners>before_flush BEGIN TRANSACTION LOGIC")
    for each_instance in a_session.dirty:
        table_name = each_instance.__tablename__  # TODO update
        # print("logic.logic_exec.listeners>before_flush flushing Dirty! "
        #      + str(table_name) + "]--> " + str(each_instance))

    for each_instance in a_session.new:
        table_name = each_instance.__tablename__
        # print("logic.logic_exec.listeners>before_flush flushing New! "
        #      + str(table_name) + "]--> " + str(each_instance))
        logic_row = LogicRow(row=each_instance, old_row=None, nest_level=0, ins_upd_dlt="ins", a_session=a_session)
        logic_row.insert(reason="client")

    print("logic.logic_exec.listeners>before_flush  END")
    # print("logic.logic_exec.listeners>before_flush  RuleBank: " + rb.__str__())
