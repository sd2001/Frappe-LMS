from config.db import Base, engine, SessionLocal
from models import sql_models as sql
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles


def create_db():
    return sql.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
def configure_templates(app):
    templates = Jinja2Templates(directory="templates")
    app.mount("/static", StaticFiles(directory="static"), name="static")
    return templates
