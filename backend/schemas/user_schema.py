from pydantic import BaseModel

class UserBase(BaseModel):
    """
    Base model for user.
    """
    username: str
    email: str
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
    password: str

class User(UserBase):
    """
    Model safe to return without the password.
    """
    id: int

    class Config:
        orm_mode = True