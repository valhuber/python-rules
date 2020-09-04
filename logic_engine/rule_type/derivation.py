from logic_engine.rule_type.rule import Rule


class Derivation(Rule):
    _column = ""  # type: str

    def __init__(self, derive: str):
        names = derive.split('.')
        # super(Second, self).__init__(*args, **kwargs)
        super(Derivation, self).__init__(names[0])
        self._column = names[1]

    def __str__(self):
        return f'Derive {self.table}.{self._column} as '
