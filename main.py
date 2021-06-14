from fastapi import FastAPI, Request
from routes import member, books, transaction, reports
import app_services.services as serv
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

# Initializing our main app
app = FastAPI(title="Frappe | LMS",
                description="API endpoints for Library Management",
                version="1.0")

# Migrating our Database migrations and configuring templates & staticfiles
serv.create_db()
templates = serv.configure_templates(app)

# Adding the Individual routers to our main app
# Adding tags to make the routes more readable(https://fastapi.tiangolo.com/tutorial/bigger-applications/)
app.include_router(member.app, tags=["Routes for Members"])
app.include_router(books.app, tags=["Routes for Books"])
app.include_router(transaction.app, tags=["Routes for Transactions"])
app.include_router(reports.app, tags=["Routes for Reports"])

# Displaying the home template
@app.get('/', include_in_schema=False)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})