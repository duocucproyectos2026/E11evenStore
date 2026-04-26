from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
import os

"""
# usar SQLite para probar si funciona
DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}  # solo para SQLite
)
"""
  
# uso de db oracle conectada a contenedor docker.
DATABASE_URL = "oracle+oracledb://system:Ora1234@127.0.0.1:1521/?service_name=freepdb1"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

#dependencia base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()