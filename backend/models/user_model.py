from sqlalchemy import Boolean, String, Integer, Column
from ..database import Base

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    is_recruiter = Column(Boolean, nullable=False, name="isrecruiter")