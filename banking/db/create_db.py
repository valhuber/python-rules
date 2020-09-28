from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base

import banking.banking_logic.models as models  #

# https://stackoverflow.com/questions/16284537/sqlalchemy-creating-an-sqlite-database-if-it-doesnt-exist

# engine = create_engine('sqlite:///banking.db', echo=True)

Base = models.Base

from banking import banking_logic

Base.metadata.create_all(banking_logic.engine)