from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import ForeignKey
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime


# Setup the database engine and session


from sqlalchemy import (create_engine, MetaData, Column, Integer, String,
        Unicode, Numeric, func, literal, select)
from sqlalchemy.orm import sessionmaker, column_property
from sqlalchemy.ext.declarative import declarative_base


#engine = create_engine('sqlite:///:memory:', echo=False)
engine = create_engine('sqlite:///piggy.db', echo=False)
session = sessionmaker(bind=engine)()

print "testing that engine works", engine.execute("select 1").scalar()

Base = declarative_base()

def get_orm_session():
    engine = create_engine('sqlite:///piggy.db', echo=False)
    session = sessionmaker(bind=engine)()
    return session 

class Account(Base):
    __tablename__ = 'accounts'
    
    id = Column(Integer, autoincrement=True, primary_key=True, unique=True)
    account_number = Column(Integer)
    amount = Column(Float)

    def __init__(self, id, account_number, amount=0):
        self.account_number = account_number
        self.amount = amount
        self.id = id

    def __repr__(self):
        #print self.zone_geom 
        #print dir(self.zone_geom)
        #for i in self.zone_geom.coords:
        #    print i
        return "<Account('%d','%d','%s')>" % (self.id, self.account_number, self.amount)
#print User.__table__

class Shared_account(Base):
    __tablename__ = 'shared_account'
    
    id = Column(Integer, autoincrement=True, primary_key=True, unique=True)
    account_id = Column(Integer, ForeignKey('accounts.id'), nullable=False  )
    tel = Column(Integer)

    def __init__(self, id, account_id, tel):
        self.id = id
        self.account_id = account_id
        self.tel = tel

    def __repr__(self):
        return "<SharedAccount('%d','%d','%d')>" % (self.id, self.account_id, self.tel)

Base.metadata.create_all(engine) 

#session.add_all([user1])

#print zone1

print engine.execute("select * from accounts").scalar()
