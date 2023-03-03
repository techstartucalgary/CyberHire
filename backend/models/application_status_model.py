from sqlalchemy import String, Integer, Column
from sqlalchemy.orm import relationship
from ..database import Base

class ApplicationStatus(Base):
    """
    Model for the application status table in the database.
    """
    __tablename__ = "application_status"

    id = Column(Integer, primary_key=True, nullable=False)
    status = Column(String(30), nullable=False, unique=True)