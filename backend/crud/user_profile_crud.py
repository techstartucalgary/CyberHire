from sqlalchemy.orm import Session
from ..models import user_profile_model
from ..schemas import user_profile_schema

def get_user_profiles(db: Session):

    return db.query(user_profile_model.UserProfile).all()

def get_user_profile_by_id(db: Session, user_id: int):

    return db.query(user_profile_model.UserProfile).filter(user_id == user_profile_model.UserProfile.user_id).first()