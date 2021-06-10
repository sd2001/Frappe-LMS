from sqlalchemy import create_engine, MetaData
import sqlalchemy.ext.declarative as declarative
import sqlalchemy.orm as orm

engine = create_engine('sqlite:///./data.db', connect_args={"check_same_thread": False})
meta = MetaData()
# conn = engine.connect()

SessionLocal = orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative.declarative_base()