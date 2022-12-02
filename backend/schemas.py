from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    email: str
    is_recruiter: bool

class User(UserBase):
    id: int
    class Config:
        orm_mode = True

class UserCreate(UserBase):
    password: str

