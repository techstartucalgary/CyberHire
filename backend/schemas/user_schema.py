from pydantic import BaseModel, EmailStr, Field

class UserBase(BaseModel):
    """
    Base model for user.
    """
    username: str = Field(max_length=100, min_length=5)
    email: EmailStr
    is_recruiter: bool

class UserInDb(UserBase):
    """
    Model for reading a user from the database.
    """
    id: int
    hashed_password: str
    class Config:
        orm_mode = True

class UserCreate(UserBase):
    """
    Model for creating a new user in the database.
    """
    password: str = Field(max_length=25, min_length=8)

    class Config:
        schema_extra = {
            "example": {
                "username": "MyUsername",
                "email": "my@example.com",
                "is_recruiter": "true",
                "password": "mySecretPassword"
            }
        }

class User(UserBase):
    """
    Model safe to return without the password.
    """
    id: int

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "username": "MyUsername",
                "email": "my@example.com",
                "is_recruiter": "true",
            }
        }