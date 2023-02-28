from sqlalchemy import String, Integer, Column, LargeBinary, ForeignKey
from ..database import Base
from sqlalchemy.orm import relationship
from .skill_model import Skill

from .user_profile_skill_model import UserProfileSkill

class UserProfile(Base):
    """
    Model for the user_profile table in the database.
    """
    __tablename__ = "user_profile"

    user_id = Column(Integer, ForeignKey("user.id"), primary_key=True, index=True, )
    first_name = Column(String(30), nullable=False)
    last_name = Column(String(30), nullable=False)
    profile_picture = Column(LargeBinary, nullable=True)
    resume = Column(LargeBinary, nullable=True)

    jobs = relationship("Job", back_populates="owner")
    skills = relationship("Skill", secondary=UserProfileSkill.__table__,  back_populates="users")
    applications = relationship("UserProfileJob", back_populates="applicant")