import sqlalchemy
from sqlalchemy import create_engine
import sys
import os

pwd=sys.path[0]
engine = create_engine('sqlite:///'+pwd+'/mydb.db?check_same_thread=False', echo=False)
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
from sqlalchemy import Column, Integer, String
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement = True,nullable =True)
    name = Column(String(50),index=True,unique=True)
    password = Column(String(20))
    time = Column(Integer,nullable=True)
    def __repr__(self):
        return "<User(name={}, password={},time={})>".format(
        self.name, self.password,self.time)
import hashlib
import time
from sqlalchemy.orm import sessionmaker
import hashlib

Session = sessionmaker(bind=engine)
session = Session()

def myhash(mystr):
    m=hashlib.md5()
    m.update(mystr.encode(encoding='utf-8'))
    return m.hexdigest()

def myhash(mystr):
    m=hashlib.md5()
    m.update(mystr.encode(encoding='utf-8'))
    return m.hexdigest()
def session_key(usr):
    tmp=time.time()
    return myhash(usr+str(tmp)),tmp
def creat_account(usr,passwd):
    try:
        ed_user = User(name=usr, password=passwd,time=int(time.time()))
        session.add(ed_user)
        session.commit()
    except Exception as error:
        print(error)
        session.rollback()
def query_user(usr):
    return session.query(User).filter_by(name=usr).first()
def renew_key(myusr):
    myusr.time=int(time.time())
    session.commit()
    return myhash(str(myusr.id+myusr.time))
def qualified(myusr,key):
    real_key=myhash(str(myusr.id+myusr.time))
    if (time.time()-myusr.time)<3600 and real_key==key:
        return True
    return False
