import os

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

BDfilename = "../SwitcherDB.sqlite"
realdir = os.path.dirname(os.path.realpath(__file__))
database_url = f"sqlite:///{os.path.join(realdir,BDfilename)}"


engine = create_engine(database_url, echo=True)

Session = sessionmaker(bind=engine)

Base = declarative_base()



