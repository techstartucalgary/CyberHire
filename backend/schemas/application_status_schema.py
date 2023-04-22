from pydantic import BaseModel, Field

class ApplicationStatusBase(BaseModel):
    """
    Base model for a job's application status.
    """

    status: str = Field(max_length=30)

class ApplicationStatus(ApplicationStatusBase):
    """
    Model for returning a job's application status.
    """

    id: int

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "status": "SUBMITTED"
            }
        }