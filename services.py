from config.db import Base, engine, SessionLocal
from models import sql_models as sql

def create_db():
	return sql.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()