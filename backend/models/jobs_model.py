from sqlalchemy import Boolean, String, Integer, Column
from ..database import Base

class Job(Base):
    """
    Model for the Jpb table in the database.
    """
    __tablename__ = "job"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(String(100), nullable=False)
    location = Column(String(100), nullable=False)
    salary = Column(Integer, nullable=False)
    skills = Column(String(100), nullable=False)