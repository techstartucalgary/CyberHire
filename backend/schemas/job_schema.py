from pydantic import BaseModel, Field
from .skill_schema import Skill
from .user_profile_schema import UserProfile

class JobBase(BaseModel):
    """
    Base model for a job.
    """

    title : str = Field(max_length=100)
    description : str = Field(max_length=2000)
    company_name : str = Field(max_length=100)
    location : str = Field(max_length=100)
    min_salary : int | None = None
    max_salary : int | None = None

class JobCreate(JobBase):
    """
    Model for creating a new job in the database.
    """

    class Config:
        schema_extra = {
            "example": {
                "title": "Junior Developer",
                "description": "Example job description here.",
                "company_name": "CyberHire",
                "location": "Calgary",
                "min_salary": 100000,
                "max_salary": 1000000
            }
        }

class JobPatch(JobBase):
    """
    Model for partial updates to a job.
    """

    title : str | None = Field(default=None, max_length=100)
    description : str | None = Field(default=None, max_length=2000)
    location : str | None = Field(default=None, max_length=100)
    company_name : str | None = Field(default=None, max_length=100)
    min_salary : int | None = None
    max_salary : int | None = None

    class Config:
        schema_extra = {
            "example": {
                "title": "Junior Developer",
                "description": "Example job description here.",
                "company_name": "CyberHire",
                "location": "Calgary",
                "min_salary": 100000,
                "max_salary": 1000000
            }
        }


class JobInDb(JobBase):
    """
    Model for updating a job in the database.
    """

    id : int
    user_profile_id : int

class Job(JobBase):
    """
    Model for returning a job.
    """

    id : int
    user_profile_id : int
    skills : list[Skill]
    owner : UserProfile

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "user_profile_id" : 1,
                "title": "Junior Developer",
                "description": "Example job description here.",
                "company_name": "CyberHire",
                "location": "Calgary",
                "min_salary": 100000,
                "max_salary": 1000000,
                "skills": [
                    {
                        "id": 1,
                        "skill": "Python"
                    }
                ],
                "owner": {
                    "user_id": 1,
                    "first_name": "John",
                    "last_name": "Doe",
                    "profile_picture": "A byte string",
                    "resume": "A byte string"
                }
            }
        }
