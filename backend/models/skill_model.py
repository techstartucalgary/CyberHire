from sqlalchemy import String, Integer, Column
from ..database import Base
from sqlalchemy.orm import relationship
from .user_profile_skill_model import UserProfileSkill
from .job_skill_model import JobSkill
from .jobs_model import Job

class Skill(Base):
    """
    Model for the skill table in the database.
    """
    __tablename__ = "skill"

    id = Column(Integer, primary_key=True, nullable=False)
    skill = Column(String(30), nullable=False, unique=True)

    users = relationship("UserProfile", secondary=UserProfileSkill.__table__, back_populates="skills")
    jobs = relationship("Job", secondary=JobSkill.__table__, back_populates="skills")