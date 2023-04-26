from pydantic import BaseModel
from datetime import date
from .application_status_schema import ApplicationStatus
from .user_profile_schema import UserProfile
from .job_schema import Job
from .application_status_schema import ApplicationStatus


class UserProfileJobBase(BaseModel):
    """
    Base model for a UserProfileJob (an application).
    """

    pass

class UserProfileJobCreate(UserProfileJobBase):
    """
    Model for creating a new UserProfileJob (an application) in the database.
    """

    pass

class UserProfileJobPatch(UserProfileJobBase):
    """
    Model for partial updates to a UserProfileJob (an application).
    """

    pass

class UserProfileJobInDb(UserProfileJobBase):
    """
    Model for updating a UserProfileJob (an application) in the database.
    """

    pass

class UserProfileJob(UserProfileJobBase):
    """
    Model for returning a UserProfileJob (an application).
    """

    user_profile_id : int
    job_id : int
    application_status_id : int
    application_submitted_date : date | None
    application_reviewed_date : date | None
    application_offer_sent_date : date | None
    application_rejected_date : date | None
    rejection_feedback : str | None
    application_status : ApplicationStatus
    applicant : UserProfile
    job: Job

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "user_profile_id": 1,
                "job_id": 1,
                "application_status_id": 1,
                "application_submitted_date": "2023-01-01",
                "application_reviewed_date": None,
                "application_offer_sent_date": None,
                "application_rejected_date": None,
                "application_status": {
                    "id": 1,
                    "status": "Application Submitted"
                },
                "applicant": {
                    "user_id": 1,
                    "first_name": "John",
                    "last_name": "Doe",
                    "profile_picture": "A byte string",
                    "resume": "A byte string"
                },
                "job": {
                    "title": "Junior Developer",
                    "description": "Example job description here.",
                    "location": "Calgary",
                    "min_salary": 100000,
                    "max_salary": 1000000
                }
            }
        }
