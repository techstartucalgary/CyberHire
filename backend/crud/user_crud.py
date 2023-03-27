from sqlalchemy.orm import Session
from passlib.context import CryptContext
from ..models import user_model
from ..schemas import user_schema

ALGORITHM = "HS256"

def get_user(db: Session, user_id: int):
    """
    Utility function to return a user object by id.

    Parameters
    ----------
    db: Session
        a database connection
    user_id: int
        the user's id in the database

    Returns
    -------
    models.user_model.User
        sqlalchemy User object
    """

    return db.query(user_model.User).filter(user_model.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    """
    Utility function to return a user by email

    Parameters
    ----------
    db: Session
        a database connection
    email: str
        the user's email address

    Returns
    -------
    Returns
    -------
    models.user_model.User
        sqlalchemy User object
    """

    return db.query(user_model.User).filter(user_model.User.email == email).first()

def get_user_by_username(db: Session, username: str):
    """
    Utility function to return a user by username

    Parameters
    ----------
    db: Session
        a database connection
    username: str
        the user's username

    Returns
    -------
    models.user_model.User
        sqlalchemy User object
    """
    
    return db.query(user_model.User).filter(user_model.User.username == username).first()

def create_user(db: Session, user: user_schema.UserCreate):
    """
    Utility function to create a user in the database

    Parameters
    ----------
    db: Session
        a database connection
    user: schemas.UserCreate
        a pydantic model representing a user to insert into the database

    Returns
    -------
    models.user_model.User
        sqlalchemy User object
    """

    ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
    hashed_password = ctx.hash(user.password)
    db_user = user_model.User(
        username=user.username,
        password=hashed_password,
        email=user.email,
        is_recruiter=user.is_recruiter
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user_by_username(db: Session, username: str):
    """
    Utility function to delete a user in the database

    Parameters
    ----------
    db: Session
        a database connection
    username: str
        a username to delete

    Returns
    -------
    models.user_model.User
        sqlalchemy User object
    """

    db_user = db.query(user_model.User).filter(user_model.User.username == username).first()
    db.delete(db_user)
    db.commit()
    return db_user

def update_user(db: Session, user: user_schema.UserInDb):
    """
    Utility function to update a user in the database
    """
    current_user = db.query(user_model.User).filter(user_model.User.id == user.id).first()
    if current_user:
        current_user.username = user.username
        current_user.password = user.hashed_password
        current_user.email = user.email
        current_user.is_recruiter = user.is_recruiter
        db.commit()
        db.refresh(current_user)
        return current_user
    
