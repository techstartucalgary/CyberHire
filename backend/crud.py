from sqlalchemy.orm import Session
from passlib.context import CryptContext
ALGORITHM = "HS256"

import models, schemas

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    ctx = CryptContext()
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