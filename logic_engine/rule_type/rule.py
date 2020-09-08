class Rule(object):

    table = None  # FIXME remove

    def __init__(self, a_table_name: str):
        #  failed -- mapped_class = get_class_by_table(declarative_base(), a_table_name)  # User class
        self.table = a_table_name
        self._dependencies = ()

    def parse_dependencies(self, rule_text: str):
        words = rule_text.split()
        for each_word in words:
            if each_word.startswith("row."):
                self._dependencies.append(each_word.split('.')[1])


    def execute(self, row, old_row, context):
        raise Exception("Not Implemented - Subclass Responsibility")