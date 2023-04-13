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

class ApplicationStatusEnum(str, Enum):

    submitted = "SUBMITTED"
    in_review = "UNDER REVIEW"
    screening = "UNDERGOING FURTHER SCREENING"
    rejected = "REJECTED"
    offer_sent = "OFFER SENT"