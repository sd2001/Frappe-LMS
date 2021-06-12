from config.db import Base, engine, SessionLocal
from models import sql_models as sql
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles


def create_db():
    '''
    Performing Database Migrations
    '''
    return sql.Base.metadata.create_all(bind=engine)

def get_db():
    '''
    Creating a Thread-Local Session to access the DB
    '''
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
def configure_templates(app):
    '''
    Configuring templates and staticfiles via Jinja2 and aiofilies respectively
    '''
    templates = Jinja2Templates(directory="templates")
    app.mount("/static", StaticFiles(directory="static"), name="static")
    return templates
