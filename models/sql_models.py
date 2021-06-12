from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Float
from sqlalchemy.orm import relationship
import datetime as dt
from config.db import Base

class Books(Base):
    __tablename__ = 'books'
    bookID = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    authors = Column(String)
    average_rating = Column(Float)
    isbn = Column(String(10), unique=True)
    isbn13 = Column(String(13), unique=True)
    language_code = Column(String)
    num_pages = Column(Integer)
    ratings_count = Column(Integer)
    text_reviews_count = Column(Integer)
    publication_date = Column(String)
    publisher = Column(String)
    total_stock = Column(Integer, default=10)
    rem_stock = Column(Integer, default=10)
    net_issue = Column(Integer, default=0)
    
    transaction = relationship('Transactions')
    

class Members(Base):
    __tablename__ = "members"
    id = Column(Integer, primary_key=True, index=True) # We should use uuid here, but to keep it simple for now I used Integer
    name = Column(String)
    email = Column(String, unique=True, index=True)
    date = Column(DateTime, default = dt.datetime.now())
    debt = Column(Integer, default=0)
    warning = Column(Boolean, default=False)
    total_spend = Column(Integer, default=0)
    transactions = relationship("Transactions")
    
class Transactions(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True) # We should use uuid here, but to keep it simple for now I used Integer  
    member_id = Column(Integer, ForeignKey('members.id'))
    book_id = Column(Integer, ForeignKey('books.bookID'))
    date = Column(DateTime, default = dt.datetime.now())
    returned = Column(Boolean, default=False)
    pay = Column(Integer, default=0)
    
    
    