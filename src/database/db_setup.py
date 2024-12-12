from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from .models import Base

DATABASE_URL = "sqlite:///gestcharge.db"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session_factory = scoped_session(Session)

def setup_database():
    Base.metadata.create_all(engine)

def get_session():
    return session_factory()
