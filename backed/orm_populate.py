import orm 
from sqlalchemy import (create_engine, MetaData, Column, Integer, String,
        Unicode, Numeric, func, literal, select)
from sqlalchemy.orm import sessionmaker, column_property
from sqlalchemy.ext.declarative import declarative_base


#engine = create_engine('sqlite:///:memory:', echo=False)
engine = create_engine('sqlite:///piggy.db', echo=False)
session = sessionmaker(bind=engine)()

acc1 = orm.Account(5000, 64, 1000)
acc2 = orm.Account(7000, 128, 10000)

shared1 = orm.SharedAccount(1,666666666)
shared2 = orm.SharedAccount(2,666666666)
shared3 = orm.SharedAccount(1,666666555)

session.add_all([acc1, acc2, shared1, shared2, shared3])
session.commit()
