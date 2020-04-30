import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
from sqlalchemy import Column, Integer, String
import sys

class Quest(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement = True,nullable =True)
    question = Column(String(1200))
    answer = Column(String(800))
    subject = Column(String(30))
    def __repr__(self):
        return "<Question={}, Answer={})>".format(
        self.question, self.answer)
pwd=sys.path[0]
engine = create_engine('sqlite:///'+pwd+'/question/question.db?check_same_thread=False', echo=False)
#Base.metadata.create_all(engine, checkfirst=True)
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()
def query_quest():
    return session.query(Quest)

