from sqlalchemy.orm import Session
from ..models import user_profile_model
from ..schemas import user_profile_schema

def get_user_profiles(db: Session):

    return db.query(user_profile_model.UserProfile).all()

def get_user_profile_by_id(db: Session, user_id: int):

    return db.query(user_profile_model.UserProfile).filter(
        user_id == user_profile_model.UserProfile.user_id).first()

def create_user_profile(
    db: Session,
    user_id: int,
    user_profile: user_profile_schema.UserProfileCreate
):

    db_user_profile = user_profile_model.UserProfile(
        user_id=user_id,
        **user_profile.dict()
    )
    db.add(db_user_profile)
    db.commit()
    db.refresh(db_user_profile)

    return db_user_profile

def update_user_resume(db: Session, user_id: int, resume: bytes | None) \
    -> user_profile_model.UserProfile | None:

    db_user_profile = db.query(user_profile_model.UserProfile) \
        .filter(user_id == user_profile_model.UserProfile.user_id) \
        .first()
        
    if db_user_profile:
        db_user_profile.resume = resume
        db.commit()
        db.refresh(db_user_profile)

        return db_user_profile

def update_user_profile_picture(db: Session, user_id: int, profile_picture: bytes | None) \
    -> user_profile_model.UserProfile | None:

    db_user_profile = db.query(user_profile_model.UserProfile) \
        .filter(user_profile_model.UserProfile.user_id == user_id) \
        .first()

    if db_user_profile:
        db_user_profile.profile_picture = profile_picture
        db.commit()
        db.refresh(db_user_profile)

    return db_user_profile