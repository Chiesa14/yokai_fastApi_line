from typing import Generator
import os
from sqlalchemy.ext.declarative import declarative_base
from sqlmodel import Session, create_engine
from sqlalchemy.orm import sessionmaker
from src.config import get_settings

db_settings = get_settings()

HOST = os.getenv("PGDB_HOST")
PORT = os.getenv("PGDB_PORT")
DB = os.getenv("PGDB_DB")
USER = os.getenv("PGDB_USER")
PASSWORD = os.getenv("PGDB_PASSWORD")

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}"
print(SQLALCHEMY_DATABASE_URL)

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db() -> Generator:
    with Session(engine) as db:
        yield db