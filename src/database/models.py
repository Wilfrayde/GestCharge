from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Material(Base):
    __tablename__ = 'materials'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    serial_number = Column(String, nullable=True)
    mac_address = Column(String, nullable=True)
    brand_model = Column(String, nullable=True)
    location = Column(String, nullable=True)
    assigned_user = Column(String, nullable=True)
    category = Column(String, nullable=True)
    assignment_date = Column(DateTime, nullable=True)
    comments = Column(String, nullable=True)
