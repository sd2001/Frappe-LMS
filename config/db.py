from sqlalchemy import create_engine, MetaData
import sqlalchemy.ext.declarative as declarative
import sqlalchemy.orm as orm
from dotenv import load_dotenv
import os
import psycopg2

load_dotenv()
DATABASE_URL = os.environ.get('DATABASE_URL')

'''
Sqlalchemy doesn't recognise postgresql as 'postgres', hence this modifies the Heroku Database URL
'''
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# -----------------------------------------------------------------

'''
Sqlalchemy Database Configurations
'''
engine = create_engine(DATABASE_URL)
meta = MetaData()
# conn = engine.connect()

SessionLocal = orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative.declarative_base()