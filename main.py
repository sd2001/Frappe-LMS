from fastapi import FastAPI, Request
from routes import member, books, transaction, reports
import services as serv
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()
templates = serv.configure_templates(app)

app.include_router(member.app)
app.include_router(books.app)
app.include_router(transaction.app)
app.include_router(reports.app)


@app.get('/', include_in_schema=False)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})