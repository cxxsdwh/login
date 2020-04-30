import sqlalchemy
from sqlalchemy import create_engine,exists
import sys
import subprocess

pwd=sys.path[0]
engine = create_engine('sqlite:///'+pwd+'/mydb.db?check_same_thread=False', echo=False)
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
from sqlalchemy import Column, Integer, String
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement = True,nullable =True)
    name = Column(String(50),index=True,unique=True)
    password = Column(String(50))
    email = Column(String(50))
    time = Column(Integer,nullable=True)
    def __repr__(self):
        return "<User(name={}, password={},email={},time={})>".format(
        self.name, self.password,self.email,self.time)
class Data(Base):
    #user data
    __tablename__ = 'datas'
    id = Column(Integer, primary_key=True,nullable=False)
    data = Column(String(2048))
    def __repr__(self):
        return "<User(id={}, data={}...)>".format(
        self.id, self.data[:50])
#Base.metadata.create_all(engine, checkfirst=True)

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

def create_account(name,password,email):
    try:
        mytime=int(time.time())
        ed_user = User(name=name, password=password,email=email,time=mytime)
        session.add(ed_user)
        session.commit()
        return myhash(str(ed_user.id)+name+mytime)
    except Exception as error:
        print(error)
        session.rollback()
        return False
def query_user(usr):
    return session.query(User).filter_by(name=usr).first()
def email_exist(addr):
    return session.query(exists().where(User.email==addr)).scalar()
def renew_key(myusr,dt=1800):
    if time.time() > (myusr.time + dt):
        myusr.time=int(time.time())
        session.commit()
    return myhash(str(myusr.id)+myusr.name+str(myusr.time))
def qualified(myusr,key):
    real_key=myhash(str(myusr.id)+myusr.name+str(myusr.time))
    if (time.time()-myusr.time)<3600 and real_key==key:
        return True
    return False
def query_data(myid):
    return session.query(Data).filter_by(id=myid).first()
def update_data(myid,mystr):
    assert len(mystr)==1600
    tmp=session.query(Data).filter_by(id=myid).first()
    if tmp:
        tmp.data=mystr
        session.commit()
    else:
        tmp=Data(id=myid,data=mystr)
        session.add(tmp)
        session.commit()
def send_mail(key,to):
    subprocess.Popen(["python3",pwd+"/send_mail.py","-k",str(key),"-t",to])
