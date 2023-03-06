from sqlalchemy import String, Integer, Column, ForeignKey
from ..database import Base
from sqlalchemy.orm import relationship
# from .skill_model import Skill
from .job_skill_model import JobSkill
from .user_profile_job_model import UserProfileJob

class Job(Base):
    """
    Model for the Job table in the database.
    """
    __tablename__ = "job"
    
    id = Column(Integer, primary_key=True, index=True)
    user_profile_id = Column(Integer, ForeignKey("user_profile.user_id"), nullable=False)
    title = Column(String(100), nullable=False)
    description = Column(String(2000), nullable=False)
    location = Column(String(100), nullable=False)
    min_salary = Column(Integer, nullable=True)
    max_salary = Column(Integer, nullable=True)

    owner = relationship("UserProfile", back_populates="jobs")
    skills = relationship("Skill", secondary=JobSkill.__table__, back_populates="jobs")
    applications = relationship("UserProfileJob", back_populates="job")