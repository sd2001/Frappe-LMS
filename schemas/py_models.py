from pydantic import BaseModel
from config.db import SessionLocal
from typing import Optional
from enum import Enum
import datetime
from models import sql_models as sql

'''
These are Pydantic Schemas for the SQL Models which are used in the routes to ensure strict Data Validation before accepting
This prevents errors within the views, resulting in Internal Server Errors(status: 500)
'''

class Members(BaseModel):
    id : int
    name : str
    email : str
    date : datetime.datetime
    debt : Optional[int] = 0
    total_spend: Optional[int] = 0
    warning : Optional[bool] = False
    
    class Config:
        orm_mode = True   # This ensures that the pydantic models can be used with the ORM: SQLAlchemy
    
class Transactions(BaseModel):
    id : int
    member_id : int
    book_id : int
    date : datetime.datetime
    returned : Optional[bool] = False
    pay : Optional[int] = 0
    class Config:
        orm_mode = True
        
class Books(BaseModel):
    bookID : int
    title : str
    authors : str
    average_rating : float
    isbn : str
    isbn13 : str
    language_code : str
    num_pages : int
    ratings_count : int
    text_reviews_count : int
    publication_date : str
    publisher : str
    total_stock : Optional[int] = 10
    rem_stock : Optional[int] = 10
    net_issue : Optional[int] = 0
    class Config:
        orm_mode = True


        

