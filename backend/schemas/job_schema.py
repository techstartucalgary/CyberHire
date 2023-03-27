from pydantic import BaseModel, Field
from .skill_schema import Skill
from .user_profile_schema import UserProfile

class JobBase(BaseModel):

    title : str = Field(max_length=100)
    description : str = Field(max_length=2000)
    company_name : str = Field(max_length=100)
    location : str = Field(max_length=100)
    min_salary : int | None = None
    max_salary : int | None = None

class JobCreate(JobBase):

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

    id : int
    user_profile_id : int

class Job(JobBase):
    
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