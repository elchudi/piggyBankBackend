import orm 
from sqlalchemy import (create_engine, MetaData, Column, Integer, String,
        Unicode, Numeric, func, literal, select)
from sqlalchemy.orm import sessionmaker, column_property
from sqlalchemy.ext.declarative import declarative_base


#engine = create_engine('sqlite:///:memory:', echo=False)
engine = create_engine('sqlite:///piggy.db', echo=False)

user1 = orm.User("666666555","token_push1")
user2 = orm.User("666666666","token_push2")


acc1 = orm.Account(5000, 64, "cerdo 1", None, 1, 10)
acc2 = orm.Account(7000, 128, "cerdo 2", None, 1, 10)
acc3 = orm.Account(8000, 256, "cerdo 3", None, 1, 10)

shared1 = orm.SharedAccount(1, 1)
shared2 = orm.SharedAccount(2, 1)
shared3 = orm.SharedAccount(1, 2)

session = sessionmaker(bind=engine)()
session.add_all([user1, user2, acc1, acc2, acc3, shared1, shared2, shared3])
session.commit()
