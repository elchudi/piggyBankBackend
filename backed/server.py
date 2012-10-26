from bottle import route, run, get, request, post
import os
import json
import orm
from json import JSONEncoder



"""
@post('/add_account')
def add_account():
    pass

    
Method should not be really implemented, only for testing purposes
"""
@get('/get_accounts')
def get_accounts():
    session = orm.get_orm_session()
    accounts = session.query(orm.Account).all()
    session.bind.dispose()
    print accounts[0]
    return accounts[0]

@get('/account_amount')
def account_amount():
    account_number = request.params.get('account_number')
    amount = get_account_amount(account_number)
    print amount
    return "".join(str(amount))

@get('/accounts_for_telephone')
def accounts_for_telephone():
    telephone = request.params.get('telephone')
    accounts =  get_accounts_for_tel(telephone)
    print accounts
    to_ret = ""
    for a in accounts:
        encoded = ORMEncoder().encode(a)
        print encoded
        #print json.dumps(a.__dict__, skipkeys=True)
        to_ret += encoded
    return to_ret

@get('/get_account')
def get_account():
    account_number = request.params.get('account_number') 
    account = get_account(account_number)   
    return ORMEncoder().encode(account)

class ORMEncoder(JSONEncoder):
    def default(self, o):
        dic = o.__dict__
        del(dic['_sa_instance_state'])
        return dic
 

def account_amount_update(account_number, amount):
    session = orm.get_orm_session()
    accounts = session.query(orm.Account).filter_by(account_number=account_number).all()
    if accounts:
        for account in accounts:
            account.amount = amount
        session.commit()
        session.bind.dispose()
        return True
    else:
        session.bind.dispose()
        return False
    
def get_account(account_number):
    session = orm.get_orm_session()
    account = session.query(orm.Account).filter_by(account_number=account_number).first()
    session.bind.dispose()
    return account

def get_account_amount(account_number):
    session = orm.get_orm_session()
    amount = session.query(orm.Account.amount).filter_by(account_number=account_number).first()
    session.bind.dispose()
    print amount
    return amount[0]

def get_account_id_from_account_number(account_number):
    session = orm.get_orm_session()
    account_id = session.query(orm.Account.id).filter_by(account_number=account_number).first()
    session.bind.dispose()
    if account_id:
        print "account_id", account_id[0]
        return account_id[0]
    return None

def get_accounts_for_tel(telephone):
    print "get_account from tel"
    session = orm.get_orm_session()
    accounts = session.query(orm.Account).join(orm.SharedAccount).join(orm.User).filter(orm.User.telephone==telephone).all()
    """
    account_ids = session.query(orm.SharedAccount.account_id).filter_by(telephone=telephone).all()
    print "accounts_ids", account_ids
    if not account_ids:
        return None
    accounts = session.query(orm.Account).filter(orm.Account.id.in_([x[0] for x in account_ids])).all()
    """
    session.bind.dispose()
    print accounts
    to_ret = []
    for acc in accounts:
        to_ret.append(acc)
    return to_ret
   
def get_tel_for_account(account_number):
    session = orm.get_orm_session()
    telephones = session.query(orm.User.telephone).join(orm.Account).filter(orm.Account.account_number==account_number).all()
    """
    account_id = get_account_id_from_account_number(account_number)
    if not account_id:
        return None
    telephones = session.query(orm.SharedAccount.telephone).filter_by(account_id=account_id).all()
    """
    session.bind.dispose()
    print telephones
    to_ret = []
    for tel in telephones:
        to_ret.append(tel[0])
    print to_ret
    return to_ret

def get_user_for_tel(telephone):
    session = orm.get_orm_session()
    users = session.query(orm.User).filter_by(telephone=telephone).all()
    session.bind.dispose()
    if users:
        return users
    return None

def add_user_to_account(account_number, telephone):
    #TODO check that there is no duplication of rows
    account_id =  get_account_id_from_account_number(account_number)
    users = get_user_for_tel(telephone)
    if users:
        print "adding", users
        shared_account =  orm.SharedAccount(account_id, users[0].id)
        session = orm.get_orm_session()
        session.add_all([shared_account])
        session.commit()
        session.bind.dispose()
        return True
    session.bind.dispose()
    return False 
 
if __name__ == "__main__":
    run(host='0.0.0.0', port=8080)
