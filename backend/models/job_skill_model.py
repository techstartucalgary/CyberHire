from sqlalchemy import Boolean, String, Integer, Column, ForeignKey
from ..database import Base
from sqlalchemy.orm import relationship

class JobSkill(Base):
    """
    Model for the job_skill table in the database.
    """
    __tablename__ = "job_skill"

    job_id = Column(Integer, ForeignKey("job.id"), nullable=False, primary_key=True)
    skill_id = Column(Integer, ForeignKey("skill.id"), nullable=False, primary_key=True)
    