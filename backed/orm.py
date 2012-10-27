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

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, autoincrement=True, primary_key=True, unique=True)
    telephone = Column(String)
    token_push = Column(String)
    
    def __init__(self, telephone, token_push):
        self.telephone = telephone
        self.token_push = token_push
    
    def __repr__(self):
        return "<User(id is'%s,'tel is '%s', token is '%s', )>" % (self.id, self.telephone, self.token_push)

class Account(Base):
    __tablename__ = 'accounts'
    
    id = Column(Integer, autoincrement=True, primary_key=True, unique=True)
    account_number = Column(String)
    amount = Column(Float)
    amount_needed = Column(Float)
    name = Column(String)
    date = Column(DateTime)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    

    def __init__(self, account_number,  amount_needed, name, date, user_id, amount=0):
        self.account_number = account_number
        self.amount = amount
        self.amount_needed = amount_needed
        self.name = name
        self.date = date
        self.user_id = user_id

    def __repr__(self):
        #print self.zone_geom 
        #print dir(self.zone_geom)
        #for i in self.zone_geom.coords:
        #    print i
        return "Account(id is '%d', acc_num'%s', amount is '%s')" % (self.id, self.account_number, self.amount)
#print User.__table__

class SharedAccount(Base):
    __tablename__ = 'shared_account'
    
    id = Column(Integer, autoincrement=True, primary_key=True, unique=True)
    account_id = Column(Integer, ForeignKey('accounts.id'), nullable=False  )
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False  )
    

    def __init__(self, account_id, user_id):
        self.account_id = account_id
        self.user_id = user_id

    def __repr__(self):
        return "<SharedAccount(id is '%d', acc_id is '%d', user id is '%d')>" % (self.id, self.account_id, self.user_id)

Base.metadata.create_all(engine) 

#session.add_all([user1])

#print zone1

accounts =  engine.execute("select * from accounts")
for row in accounts:
    print row
accounts =  engine.execute("select * from shared_account")
for row in accounts:
    print row

