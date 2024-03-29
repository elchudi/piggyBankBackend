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
    for a in accounts:
        print a
    return accounts

def get_shared_accounts():
    session = orm.get_orm_session()
    accounts = session.query(orm.SharedAccount).all()
    session.bind.dispose()
    for a in accounts:
        print a
    return accounts

def get_users():
    session = orm.get_orm_session()
    accounts = session.query(orm.User).all()
    session.bind.dispose()
    for a in accounts:
        print a
    return accounts

@get('/account_amount')
def account_amount():
    account_number = request.params.get('account_number')
    amount = get_account_amount(account_number)
    print amount
    return "".join(str(amount))

@post('/accounts_for_telephone')
def accounts_for_telephone():
    telephone = request.json['telephone']
    accounts =  get_accounts_for_tel(telephone)
    print "found these accounts", accounts
    to_ret = '{"piggy":[ '
    if accounts:
        for a in accounts:
            telephones = get_tels_for_account(a.account_number)
            encoded = ORMEncoder().encode(a)
            encoded = encoded[:-1]
            encoded += ',"telephones":['
            for t in telephones :
                encoded += '{"telephone":'
                encoded += t
                encoded += '},'
            encoded = encoded[:-1]
            encoded += ']}'
            print encoded
            #print json.dumps(a.__dict__, skipkeys=True)
            to_ret += encoded
            to_ret += ","
    to_ret = to_ret[:-1]
    to_ret += ']}'
    print to_ret
    return to_ret

@post('/my_accounts')
def my_accounts_get():
    telephone = request.json['telephone']
    print telephone
    accounts =  my_accounts(telephone)
    print accounts
    to_ret = '{"piggy":[ '
    for a in accounts:
        telephones = get_tels_for_account(a.account_number)
        encoded = ORMEncoder().encode(a)
        encoded = encoded[:-1]
        encoded += ',"telephones":['
        for t in telephones :
            encoded += '{"telephone":'
            encoded += t
            encoded += '},'
        encoded = encoded[:-1]
        encoded += ']}'
        print encoded
        #print json.dumps(a.__dict__, skipkeys=True)
        to_ret += encoded
        to_ret += ","
    to_ret = to_ret[:-1]
    to_ret += ']}'
    print to_ret
    return to_ret

@get('/get_account')
def get_account():
    account_number = request.params.get('account_number') 
    account = get_account(account_number)   
    return ORMEncoder().encode(account)

@post('/update_account_amount')
def update_account_amount():
    account_number =  request.json['account_number']
    amount = request.json['amount']
    return str(account_amount_update(account_number, amount))

@post('/add_user_to_account')
def add_user_to_account():
    print "add 1"
    telephone = request.json['telephone']
    print "add 2"
    account_number = request.json['account_number']
    print "REST with", telephone, account_number
    return str(add_user_to_account_real(account_number, telephone))


@post('/add_user')
def add_user():
    print "adding user"
    print request.json
    print dir(request.json)
    telephone = request.json['telephone']
    token = request.json['token']
    session = orm.get_orm_session()
    user = orm.User(telephone, token)
    session.add_all([user])
    session.commit()
    session.bind.dispose()
    print "useradde ", telephone, token
    return "OK"

def add_user_simple(tel, tok="toke"):
    session = orm.get_orm_session()
    user = orm.User(tel, tok)
    session.add_all([user])
    session.commit()
    session.bind.dispose()
    return user
    
@post('/add_account')
def add_account():
    print "adding account"
    print request.json
    print dir(request.json)
    telephone = request.json['telephone']
    name = request.json['name']
    amount = request.json['amount']
    amount_needed = request.json['amount_needed']
    account_number = request.json['account_number']
    
    session = orm.get_orm_session()
    user_id = get_user_for_tel(telephone)[0].id
    acc = orm.Account( account_number,  amount_needed, name, None, user_id, amount)
    session.add_all([acc])
    session.commit()
    acc = get_account(account_number)
    shared_acc = orm.SharedAccount( acc.id, user_id)
    session.add_all([shared_acc])
    session.commit()
    session.bind.dispose()
    print "account added ", telephone, account_number
    return "OK"


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
    print "get_account from tel", telephone
    session = orm.get_orm_session()
    user = get_user_for_tel(telephone)
    if not user:
        print "user not found returning none"
        return None
    for u in user:
        print "u", u    
    print user, user[0].id
    
    #accounts = session.query(orm.Account).join(orm.SharedAccount).join(orm.User).filter(orm.User.telephone==telephone).all()
    account_ids = session.query(orm.SharedAccount.account_id).filter_by(user_id=user[0].id).all()
    print "accounts_ids", account_ids
    if not account_ids:
        return None
    accounts = session.query(orm.Account).filter(orm.Account.id.in_([x[0] for x in account_ids])).all()
    session.bind.dispose()
    print "accounts", accounts
    to_ret = []
    for acc in accounts:
        to_ret.append(acc)
    return to_ret
   
def my_accounts(telephone):
    session = orm.get_orm_session()
    accounts = session.query(orm.Account).join(orm.User).filter(orm.User.telephone==telephone).all()
    print "my accounts", accounts
    session.bind.dispose()
    if accounts:
        return accounts 
    return None

def get_tels_for_account(account_number):
    session = orm.get_orm_session()
    account_id =  get_account_id_from_account_number(account_number)
    telephones = session.query(orm.User.telephone).join(orm.SharedAccount).filter(orm.SharedAccount.account_id==account_id).all()
    """
    account_id = get_account_id_from_account_number(account_number)
    if not account_id:
        return None
    telephones = session.query(orm.SharedAccount.telephone).filter_by(account_id=account_id).all()
    """
    session.bind.dispose()
    print "telephones are", telephones
    to_ret = []
    for tel in telephones:
        to_ret.append(tel[0])
    print "toretraro", to_ret
    return to_ret

def get_user_for_tel(telephone):
    session = orm.get_orm_session()
    users = session.query(orm.User).filter_by(telephone=telephone).all()
    session.bind.dispose()
    if users:
        return users
    return None

def add_user_to_account_real(account_number, telephone):
    #TODO check that there is no duplication of rows
    print "adding user to account and telephone", account_number, telephone
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
