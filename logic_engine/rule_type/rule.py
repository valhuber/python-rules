class Rule(object):

    table = None  # FIXME remove

    def __init__(self, a_table_name: str):
        #  failed -- mapped_class = get_class_by_table(declarative_base(), a_table_name)  # User class
        self.table = a_table_name
        self.dependencies = ()

    def execute(self, row, old_row, context):
        raise Exception("Not Implemented - Subclass Responsibility")