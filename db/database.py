from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sqlite3

SQLALCHEMY_DATABASE_URL = 'sqlite:///./task_managementDB.db'
 
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Enable foreign keys for SQLite
@event.listens_for(engine, "connect")
def enable_foreign_keys(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, sqlite3.Connection):  # only for SQLite
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close() 
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
 
Base = declarative_base()
 
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()