from enum import Enum

from sqlalchemy import String, Integer, Column
from ..database import Base

class ApplicationStatus(Base):
    """
    Model for the application status table in the database.
    """
    __tablename__ = "application_status"

    id = Column(Integer, primary_key=True, nullable=False)
    status = Column(String(30), nullable=False, unique=True)

class ApplicationStatusEnum(int, Enum):

    submitted = 1
    in_review = 2
    screening = 3
    rejected = 4
    offer_sent = 5