import requests
from fastapi import APIRouter, Depends, HTTPException, Response
from schemas  import py_models as pm
from typing import List
import services as serv
import sqlalchemy.orm as orm
from models import sql_models as sql

app = APIRouter()



@app.get('/books/push_db', status_code = 201)
def push_db(db: orm.Session=Depends(serv.get_db)):
    try:
        booklist = requests.get('https://frappe.io/api/method/frappe-library')
        books = booklist.json()
        books = books["message"]
        for book in books:
            new_book = sql.Books(
                bookID = book['bookID'],
                title = book['title'],
                authors = book['authors'],
                average_rating = book['average_rating'],
                isbn = book['isbn'],
                isbn13 = book['isbn13'],
                language_code = book['language_code'],
                num_pages = book['  num_pages'],
                ratings_count = book['ratings_count'],
                text_reviews_count = book['text_reviews_count'],
                publication_date = book['publication_date'],
                publisher = book['publisher'],        
            )
            db.add(new_book)
            db.commit()
            db.refresh(new_book)
        return Response(content="Data has been Added")
    except Exception as e:
        return Response(content=str(e))
     

@app.get('/books', response_model=List[pm.Books])
def getbooks(db: orm.Session=Depends(serv.get_db)):
    try:
        db_books = db.query(sql.Books).all()
        return db_books
    except Exception as e:
        return Response(content=str(e))

@app.get('/books/{id}', response_model=pm.Books)
def getbook(id: int, db: orm.Session=Depends(serv.get_db)):
    try:
        db_book = db.query(sql.Books).filter(sql.Books.bookID == id).first()
        if db_book is None:
            raise HTTPException(status_code=404, detail="This book does not exist!")
        return db_book
    except Exception as e:
        return Response(content=str(e))