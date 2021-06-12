from fastapi import APIRouter, Depends, HTTPException
from schemas  import py_models as pm
from typing import List
import services as serv
import sqlalchemy.orm as orm
from models import sql_models as sql

app = APIRouter()

@app.post('/transaction/new_issue', status_code = 201, response_model=pm.Transactions)
async def new_issue(transaction: pm.Transactions, db: orm.Session=Depends(serv.get_db)):
    transaction_member = db.query(sql.Members).filter(sql.Members.id == transaction.member_id).first()
    transaction_book = db.query(sql.Books).filter(sql.Books.bookID == transaction.book_id).first()
    if transaction_book is None:
        raise HTTPException(status_code=404, detail="This Book ID doesn't exist!")
    
    if transaction_member is None:
        raise HTTPException(status_code=404, detail="This Member ID doesn't exist!")
    
    db_user = db.query(sql.Members).filter(sql.Members.id == transaction.member_id).first()
    
    if db_user.warning == True:
        raise HTTPException(status_code=403, detail="Member Debt exceeds Limit, Forbidden!")
    
    db_book = db.query(sql.Books).filter(sql.Books.bookID == transaction.book_id).first()
    if db_book.rem_stock == 0:
        raise HTTPException(status_code=406, detail="Book Out of Stock!")
        
    new_transaction = sql.Transactions(member_id=transaction.member_id, book_id=transaction.book_id)
    db_book.rem_stock -= 1
    db_book.net_issue += 1
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)
    db.refresh(db_book)
    return new_transaction

@app.put('/transaction/new_issue/{id}', response_model=pm.Transactions)
async def return_issue(id:int, transaction: pm.Transactions, db: orm.Session=Depends(serv.get_db)):    
    db_transac = db.query(sql.Transactions).filter(sql.Transactions.id == id).first()
    if db_transac is None:
        raise HTTPException(status_code=404, detail="This Transaction ID does not exist!")
    if db_transac.returned == False and transaction.returned == True:
        db_transac.returned = True
        db.commit()
        db.refresh(db_transac) 
    
    db_book = db.query(sql.Books).filter(sql.Books.bookID == db_transac.book_id).first()
    db_book.rem_stock += 1
    
    db_transac.pay = transaction.pay
    db_member_id = db_transac.member_id
    db_user = db.query(sql.Members).filter(sql.Members.id == db_member_id).first()
    db_user.total_spend += transaction.pay
    
    if db_transac.pay != 50:
        db_user.debt += 50 - db_transac.pay
        
    if db_user.debt > 500 and db_user.warning == False:
        db_user.warning = True
        
    db.commit()
    db.refresh(db_transac)    
    db.refresh(db_user)    
    db.refresh(db_book)    
    return db_transac

@app.get('/transactions', response_model=List[pm.Transactions])
async def get_transactions(db: orm.Session=Depends(serv.get_db)):
    db_transac = db.query(sql.Transactions).all()
    return db_transac