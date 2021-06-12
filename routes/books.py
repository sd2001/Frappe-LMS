import requests
from fastapi import APIRouter, Depends, HTTPException, Response
from schemas  import py_models as pm
from typing import List
import app_services.services as serv
import sqlalchemy.orm as orm
from models import sql_models as sql

app = APIRouter()


@app.get('/books/push_db', status_code = 201)
def push_db(db: orm.Session=Depends(serv.get_db)):
    '''
    This route pushes the Data from Frappe API into the database directly. This also ensures the entries aren't duplicated.
    The data obtained is stored in the Books Table respective to their Column Labels
    '''
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
    except Exception:
        return Response(content="Books have already been added!")
    
     

@app.get('/books', response_model=List[pm.Books])
def getbooks(db: orm.Session=Depends(serv.get_db)):
    '''
    This route fetches all the existing books from the Database and shows it to the user in form of a list.
    This includes sensitive details like the BookID, Stocks and the No of Issues.
    For the Librarian!
    '''
    try:
        db_books = db.query(sql.Books).all()
        return db_books
    except Exception as e:
        return Response(content=str(e))
    
@app.get('/members/views/books', response_model=List[pm.Books],
         response_model_exclude={"bookID", "total_stock", "rem_stock", "net_issue"})
def member_session_books(db: orm.Session=Depends(serv.get_db)):
    '''
    This route fetches all the existing books from the Database and shows it to the user in form of a list.
    This doesn't reveal sensitive details like the BookID, Stocks and the No of Issues.
    For the Members or the Users!
    '''
    try:
        db_books = db.query(sql.Books).all()
        return db_books
    except Exception as e:
        return Response(content=str(e))

@app.get('/books/{id}', response_model=pm.Books)
def getbook(id: int, db: orm.Session=Depends(serv.get_db)):
    '''
    This route fetches a single book from the Database as per the entered BookID.
    This includes sensitive details like the BookID, Stocks and the No of Issues.
    For the Librarian!
    '''    
    db_book = db.query(sql.Books).filter(sql.Books.bookID == id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="This book does not exist!")
    return db_book
    