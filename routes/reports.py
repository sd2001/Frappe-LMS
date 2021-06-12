from fastapi import APIRouter, Depends, HTTPException, Response, Request
from schemas  import py_models as pm
from typing import List
import services as serv
import sqlalchemy.orm as orm
from sqlalchemy import distinct
from models import sql_models as sql
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
import numpy as np
from charts import combined_trace as ct
from fastapi.templating import Jinja2Templates


app = APIRouter()
templates = Jinja2Templates(directory="templates")

@app.get('/reports')
async def get_report(request: Request, db: orm.Session=Depends(serv.get_db)):
    db_dist_books = db.query(sql.Transactions.book_id.distinct())
    db_dist_members = db.query(sql.Transactions.member_id.distinct())
    # print(db_dist_members.count())
    
    members_name = list()
    members_spending = list()
    books_names = list()
    books_issues = list()
    
    for b in db_dist_members.all():
        db_member = db.query(sql.Members).filter(sql.Members.id == b[0]).first()
        member_spend = db_member.total_spend
        members_name.append(db_member.name)
        members_spending.append(member_spend)
        
    for b in db_dist_books.all():
        db_book = db.query(sql.Books).filter(sql.Books.bookID == b[0]).first()
        book_issue = db_book.net_issue
        books_names.append(db_book.title)        
        books_issues.append(book_issue)        
    
    members_name = np.array(members_name)
    members_spending = np.array(members_spending)
    books_names = np.array(books_names)
    books_issues = np.array(books_issues)
    
    ct.final_plots(members_name, members_spending, books_names, books_issues)
    
    return templates.TemplateResponse("chart.html", {"request": request})
    
    
 


    

    