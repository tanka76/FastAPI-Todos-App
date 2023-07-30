import sys
import psycopg2
from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
import os,sys
from dotenv import load_dotenv

BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR,".env"))
sys.path.append(BASE_DIR)


DATABASE_URL = os.environ["DATABASE_URL"]

engine = create_engine(
    DATABASE_URL
)
# engine = create_engine(
#     DBSettings.SQLALCHEMY_DATABASE_URL, pool_size=10,
#     max_overflow=2,
#     pool_recycle=300,
#     pool_pre_ping=True,
#     pool_use_lifo=True
# )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) 

Base = declarative_base() 

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()