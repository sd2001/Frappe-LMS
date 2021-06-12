from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Float
from sqlalchemy.orm import relationship
import datetime as dt
from config.db import Base

class Books(Base):
    '''
    Books and their meta-data as obtained from the Frappe API : https://frappe.io/api/method/frappe-library
    '''
    __tablename__ = 'books'
    bookID = Column(Integer, primary_key=True, index=True) # We should use uuid here, but to keep it simple for now I used Integer
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
    total_stock = Column(Integer, default=10)  # Record of the total stocks for the Book
    rem_stock = Column(Integer, default=10)  # Record of the remaining stocks for the Book
    net_issue = Column(Integer, default=0)   # Record of the total issues for the Book
    
    transaction = relationship('Transactions')
    

class Members(Base):
    __tablename__ = "members"
    id = Column(Integer, primary_key=True, index=True) # We should use uuid here, but to keep it simple for now I used Integer
    name = Column(String)
    email = Column(String, unique=True, index=True)
    date = Column(DateTime, default = dt.datetime.now())
    debt = Column(Integer, default=0)    # Keeps a note of the pending amount for each transaction
    warning = Column(Boolean, default=False)  # Bool value to check if debt exceeds 500 bucks
    total_spend = Column(Integer, default=0)  # Total Expenditure for the Member
    transactions = relationship("Transactions")  # One to One Relationship with Transactions
    
class Transactions(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True) # We should use uuid here, but to keep it simple for now I used Integer  
    member_id = Column(Integer, ForeignKey('members.id'))
    book_id = Column(Integer, ForeignKey('books.bookID'))
    date = Column(DateTime, default = dt.datetime.now())
    returned = Column(Boolean, default=False)  # Keeps a check on whether the book is returned or not
    pay = Column(Integer, default=0)   # Keeps a check on the amount paid on return of Book
    
    
    