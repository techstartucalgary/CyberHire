from sqlalchemy import String, Integer, Column
from ..database import Base
from sqlalchemy.orm import relationship
from .user_profile_skill_model import UserProfileSkill

class Skill(Base):
    """
    Model for the skill table in the database.
    """
    __tablename__ = "skill"

    id = Column(Integer, primary_key=True, nullable=False)
    skill = Column(String(30), nullable=False, unique=True)

    users = relationship("UserProfile", secondary=UserProfileSkill.__table__, back_populates="skills")

