from pydantic import BaseModel, Field

class SkillBase(BaseModel):
    """
    Base model for skill.
    """
    skill: str = Field(max_length=30)

class Skill(SkillBase):
    """
    Model to return a skill.
    """

    id: int

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "skill": "Python"
            }
        }