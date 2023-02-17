from pydantic import BaseModel
from .skill_schema import Skill

class UserProfileBase(BaseModel):
    """
    Base model for a user profile.
    """

    first_name: str
    last_name: str

class UserProfileCreate(UserProfileBase):
    """
    Model for creating a new user profile in the database.
    """

    class Config:
        schema_extra = {
            "example": {
                "first_name": "John",
                "last_name": "Doe"
            }
        }

class UserProfilePatch(UserProfileBase):
    """
    Model for partial updates to a user profile.
    """

    first_name: str | None = None
    last_name: str | None = None

    class Config:
        schema_extra = {
            "example": {
                "first_name": "John",
                "last_name": "Doe"
            }
        }

class UserProfileInDB(UserProfileBase):
    """
    Model for updating a user profile in the database.
    """
    user_id: int

class UserProfile(UserProfileBase):
    """
    Model for returning a user profile.
    """

    user_id: int
    skills: list[Skill]

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "user_id": 1,
                "first_name": "John",
                "last_name": "Doe",
                "profile_picture": "A byte string",
                "resume": "A byte string"
            }
        }