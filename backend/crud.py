from sqlalchemy.orm import Session
from passlib.context import CryptContext
ALGORITHM = "HS256"

import models, schemas

def get_user(db: Session, user_id: int):
    """
    Utility function to return a user object by id.

    db: Session
        a database connection
    user_id: int
        the user's id in the database
    """

    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    """
    Utility function to return a user by email

    db: Session
        a database connection
    email: str
        the user's email address
    """

    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_username(db: Session, username: str):
    """
    Utility function to return a user by username

    db: Session
        a database connection
    username: str
        the user's username
    """
    
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    """
    Utility function to create a user in the database

    db: Session
        a database connection
    user: schemas.UserCreate
        a pydantic model representing a user to insert into the database
    """

    ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
    hashed_password = ctx.hash(user.password)
    db_user = models.User(
        username=user.username,
        password=hashed_password,
        email=user.email,
        is_recruiter=user.is_recruiter
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user