import sys
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os,sys
from conf.config import setting


engine = create_engine(
    setting.DATABASE_URL
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