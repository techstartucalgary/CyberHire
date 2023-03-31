from pydantic import BaseModel, Field

class ApplicationStatusBase(BaseModel):

    status: str = Field(max_length=30)

class ApplicationStatus(ApplicationStatusBase):

    id: int

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "status": "SUBMITTED"
            }
        }