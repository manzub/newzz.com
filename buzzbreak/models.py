from datetime import datetime
from sqlalchemy.sql.sqltypes import DateTime
from buzzbreak import db
from sqlalchemy import Column,String,Text,Integer,ForeignKey
from sqlalchemy.orm import relationship,backref
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from buzzbreak import login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# CREATE MODELS
class User(db.Model,UserMixin):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True)
    email = Column(Text)
    password = Column(Text)
    account = relationship('Accounts',backref='users',lazy=True,cascade="all, delete-orphan")
    payopt = relationship('PayOpt',backref='users',lazy=True,cascade="all, delete-orphan")
    transactions = relationship('Transactions',backref='users',lazy=True,cascade="all, delete-orphan")

    def __init__(self,email,password):
        self.email = email
        self.password = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password,password)

class Accounts(db.Model,UserMixin):
    __tablename__ = "accounts"
    id = Column(Integer,primary_key=True)
    balance = Column(String)
    t_balance = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))

    def __init__(self,balance,t_balance,user_id):
        self.balance = balance
        self.t_balance = t_balance
        self.user_id = user_id

class PayOpt(db.Model,UserMixin):
    __tablename__ = 'payopts'
    id = Column(Integer,primary_key=True)
    type = Column(Integer)
    payment_email = Column(String)
    extras = Column(Text)
    user_id = Column(Integer, ForeignKey('users.id'))

    def __init__(self,type,payment_email,user_id,extras):
        self.type = type
        self.payment_email = payment_email
        self.user_id = user_id
        self.extras = extras

class Transactions(db.Model,UserMixin):
    __tablename__ = 'transactions'
    id = Column(Integer,primary_key=True)
    user_id = Column(Integer,ForeignKey('users.id'))
    alert = Column(Text)
    extras = Column(String(100))

    def __init__(self,alert,extras,user_id):
        self.alert = alert
        self.user_id = user_id
        self.extras = extras

class Cashouts(db.Model,UserMixin):
    __tablename__ = 'cashouts'
    id = Column(Integer,primary_key=True)
    user_email = Column(String)
    amount = Column(String)
    payout_type = Column(String)

    def __init__(self,user_email,amount,payout_type):
        self.user_email = user_email
        self.amount = amount
        self.payout_type = payout_type

class Tokens(db.Model,UserMixin):
    __tablename__ = 'tokens'
    id = Column(Integer,primary_key=True)
    user_email = Column(String)
    token = Column(Text)
    expires = Column(DateTime,default=datetime.utcnow)

    def __init__(self,user_email,token):
        self.user_email = user_email
        self.token = token
