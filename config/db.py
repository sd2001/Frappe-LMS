from sqlalchemy import create_engine, MetaData
import sqlalchemy.ext.declarative as declarative
import sqlalchemy.orm as orm
from dotenv import load_dotenv
import os
import psycopg2

load_dotenv()
DATABASE_URL = os.environ.get['DATABASE_URL']

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
meta = MetaData()
# conn = engine.connect()

SessionLocal = orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative.declarative_base()