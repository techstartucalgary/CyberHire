from pydantic import BaseModel
from fastapi import Form, File, Depends
from .skill_schema import Skill

class UserProfileBase(BaseModel):
    """
    Base model for a user profile.
    """

    first_name: str
    last_name: str
    profile_picture: bytes | None = None
    resume: bytes | None = None

    def __init__(
        self,
        first_name: str = Form(),
        last_name: str = Form(),
        profile_picture: bytes | None = File(default=None),
        resume: bytes | None = File(default=None)
    ):
        self.first_name = first_name
        self.last_name = last_name
        self.profile_picture = profile_picture
        self.resume = resume

class UserProfileCreate(UserProfileBase):
    """
    Model for creating a new user profile in the database.
    """

    def __init__(self, base: UserProfileBase = Depends(UserProfileBase)):
        super().__init__(base.first_name, base.last_name, base.profile_picture, base.resume)

    class Config:
        schema_extra = {
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "profile_picture": "A byte string",
                "resume": "A byte string"
            }
        }

class UserProfilePatch(UserProfileBase):
    """
    Model for partial updates to a user profile.
    """

    first_name: str | None = None
    last_name: str | None = None
    profile_picture: bytes | None = None
    resume: bytes | None = None

    def __init__(
        self,
        first_name: str | None = Form(default=None),
        last_name: str | None = Form(default=None),
        profile_picture: bytes | None = File(default=None),
        resume: bytes | None = File(default=None)
    ):
        self.first_name = first_name
        self.last_name = last_name
        self.profile_picture = profile_picture
        self.resume = resume

    class Config:
        schema_extra = {
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "profile_picture": "A byte string",
                "resume": "A byte string"
            }
        }

class UserProfile(UserProfileBase):
    """
    Model for returning a user profile.
    """

    id: int
    skills: list[Skill]

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "first_name": "John",
                "last_name": "Doe",
                "profile_picture": "A byte string",
                "resume": "A byte string"
            }
        }