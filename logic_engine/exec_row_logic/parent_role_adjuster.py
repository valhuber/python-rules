from logic_engine.exec_row_logic.logic_row import LogicRow


class ParentRoleAdjuster:
    """
    Passed to <aggregate>.adjust_parent who will set parent row(s) values
    iff adjustment is required (e.g., summed value changes, where changes, fk changes, etc)
    This ensures only 1 update per set of aggregates along a given role
    """

    def __init__(self, parent_role_name: str, child_logic_row: LogicRow):

        self.child_logic_row = child_logic_row  # the child (curr, old values)

        self.parent_role_name = parent_role_name  # which parent are we dealing with?
        self.parent_logic_row = None
        self.previous_parent_logic_row = None

    def save_altered_parents(self):
        if self.parent_logic_row is None:  # save *only altered* parents (often does nothing)
            print("adjust not required for parent_logic_row: " + str(self))
        else:
            print("adjust required for parent_logic_row: " + str(self))

        if self.previous_parent_logic_row is None:
            print("save adjusted not required for previous_parent_logic_row: " + str(self))
        else:
            raise Exception("Not Implemented - adjust required for parent_logic_row: " + str(self))
