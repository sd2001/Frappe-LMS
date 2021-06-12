from fastapi import FastAPI
from routes import member, books, transaction, reports
import services as serv

app = FastAPI()

serv.create_db()

app.include_router(member.app)
app.include_router(books.app)
app.include_router(transaction.app)
app.include_router(reports.app)