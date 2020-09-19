from __future__ import annotations
from typing import List, TypeVar, Dict

from sqlalchemy.engine import base
from sqlalchemy.ext.declarative import declarative_base

from logic_engine.exec_row_logic.logic_row import LogicRow


class RowCache():

    def __init__(self):
        self.row_list = {}  # type: Dict[base, 'LogicRow']

    def add(self, logic_row: 'LogicRow'):
        if logic_row.row not in self.row_list:
            self.row_list[logic_row.row] = logic_row