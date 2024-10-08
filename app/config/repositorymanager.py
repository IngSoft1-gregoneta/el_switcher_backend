import os

from sqlalchemy import (
    create_engine
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

BDfilename = "../SwitcherDB.sqlite"
realdir = os.path.dirname(os.path.realpath(__file__))
database_url = f"sqlite:///{os.path.join(realdir,BDfilename)}"


engine = create_engine(database_url, echo=False)

Session = sessionmaker(bind=engine)

Base = declarative_base()

