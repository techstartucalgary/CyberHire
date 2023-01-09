from sqlalchemy import Integer, Column, ForeignKey, UniqueConstraint
from ..database import Base

class UserProfileSkill(Base):
    """
    Model for the user_profile_skill many to many linking table in the databse.
    """
    __tablename__ = "user_profile_skill"
    __table_args__ = (
        UniqueConstraint(
            "user_profile_id",
            "skill_id"
        ),
    )

    user_profile_id = Column(Integer, ForeignKey("user_profile.user_id"), nullable=False, primary_key=True)
    skill_id = Column(Integer, ForeignKey("skill.id"), nullable=False, primary_key=True)