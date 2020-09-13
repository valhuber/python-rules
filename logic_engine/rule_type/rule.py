class Rule(object):
    table = None  # FIXME remove

    def __init__(self, a_table_name: str):
        #  failed -- mapped_class = get_class_by_table(declarative_base(), a_table_name)  # User class
        self.table = a_table_name
        self._dependencies = ()

    def parse_dependencies(self, rule_text: str):
        """
        Split rule_text into space-separated words
        Set <rule>._dependencies() to all words starting with "row."
        """
        words = rule_text.split()
        for each_word in words:
            if each_word.startswith("row."):  # allow Cust.CreditLimit?
                dependencies = each_word.split('.')
                if len(dependencies) == 2:
                    self._dependencies.append(dependencies[1])
                else:
                    self._dependencies.append(dependencies[1] +
                                              "." + dependencies[2])
