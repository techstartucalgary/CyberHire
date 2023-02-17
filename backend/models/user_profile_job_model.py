from sqlalchemy import Boolean, String, Integer, Column, ForeignKey, Date
from ..database import Base
from sqlalchemy.orm import relationship

class UserProfileJob(Base):
    """
    Model for the user_profile_job many to many linking table in the database
    """

    user_profile_id = Column(Integer, ForeignKey("user_profile.user_id"), nullable=False, primary_key=True)
    job_id = Column(Integer, ForeignKey("job.id"), nullable=False, primary_key=True)
    application_status_id = Column(Integer, ForeignKey("application_status.id"), nullable=False)
    application_submitted_date = Column(Date, nullable=False)
    application_reviewed_date = Column(Date, nullable=True)
    application_offer_sent_date = Column(Date, nullable=True)
    application_rejected_date =Column(Date, nullable=True)

    application_status = relationship("ApplicationStatus")