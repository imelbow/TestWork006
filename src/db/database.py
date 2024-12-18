from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
import time

from core.config import get_settings
from .models import Base

def get_database_engine():
    retries = 5
    while retries > 0:
        try:
            engine = create_engine(
                get_settings().DATABASE_URL,
                pool_pre_ping=True,
                connect_args={
                    "connect_timeout": 5
                }
            )
            Base.metadata.create_all(bind=engine)
            return engine
        except OperationalError as e:
            retries -= 1
            if retries == 0:
                raise Exception(
                    f"Failed to connect to database after 5 attempts: {str(e)}"
                )
            time.sleep(2)

engine = get_database_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
