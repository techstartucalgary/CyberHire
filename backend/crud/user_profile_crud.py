from sqlalchemy.orm import Session
from ..models import user_profile_model
from ..schemas import user_profile_schema

def get_user_profiles(db: Session):
    """
    Utility function to return all user profiles in the database

    Parameters
    ----------
    db: Session
        a database session

    Returns
    -------
    list[models.user_profile_model.UserProfile]
        list of sqlalchemy UserProfile objects
    """

    return db.query(user_profile_model.UserProfile).all()

def get_user_profile_by_id(db: Session, user_id: int) \
        -> user_profile_model.UserProfile | None:
    """
    Utility function to return a user profile by user id

    Parameters
    ----------
    db: Session
        a database session
    user_id: int
        the user's id in the datbase

    Returns
    -------
    models.user_profile_model.UserProfile
        sqlalchemy UserProfile object
    """

    return db.query(user_profile_model.UserProfile)\
        .filter(user_id == user_profile_model.UserProfile.user_id).first()

def create_user_profile(db: Session, user_id: int,
        user_profile: user_profile_schema.UserProfileCreate):
    """
    Utility function to create a new user profile for the user with
    user id = user_id.

    Parameters
    ----------
    db: Session
        a database session
    user_id: int
        the user's id in the database
    user_profile: schemas.user_profile_schema.UserProfileCreate
        a pydantic model for creating a new user profile

    Returns
    -------
    models.user_profile_model.UserProfile
        a sqlalchemy UserProfile object representing the newly created user profile
    """

    db_user_profile = user_profile_model.UserProfile(
        user_id=user_id, **user_profile.dict())
    db.add(db_user_profile)
    db.commit()
    db.refresh(db_user_profile)

    return db_user_profile

def delete_user_profile(db: Session, user_id: int):
    """
    Utility function to delete a user profile from the database.

    Parameters
    ----------
    db: Session
        a database session
    user_id: int
        the user's id in the database
    
    Returns
    -------
    models.user_profile_model.UserProfile
        a sqlalchemy UserProfile object representing the deleted user profile
    """

    db_user_profile = db.query(user_profile_model.UserProfile) \
        .filter(user_profile_model.UserProfile.user_id == user_id).first()
    db.delete(db_user_profile)
    db.commit()

    return db_user_profile

def update_user_resume(db: Session, user_id: int, resume: bytes | None) \
        -> user_profile_model.UserProfile | None:
    """
    Utility function to update a user's resume in the database. User must
    have a user profile.

    Parameters
    ----------
    db: Session
        a database session
    user_id: int
        the user's id in the database
    resume: bytes | None
        the user's resume or None to remove the resume in the database

    Returns
    -------
    models.user_profile_model.UserProfile
        a sqlalchemy UserProfile object representing the updated user profile
    """

    db_user_profile = db.query(user_profile_model.UserProfile) \
        .filter(user_id == user_profile_model.UserProfile.user_id) \
        .first()
        
    if db_user_profile:
        db_user_profile.resume = resume
        db.commit()
        db.refresh(db_user_profile)

        return db_user_profile

def update_user_profile_picture(db: Session, user_id: int,
        profile_picture: bytes | None) -> user_profile_model.UserProfile | None:
    """
    Utility function to update a user's profile picture in the database. User must
    have a user profile.

    Parameters
    ----------
    db: Session
        a database session
    user_id: int
        the user's id in the database
    profile_picture: bytes | None
        the user's profile picture or None to remove the profile picture in the database

    Returns
    -------
    models.user_profile_model.UserProfile
        sql alchemy object representing the updated user profile
    """
    db_user_profile = db.query(user_profile_model.UserProfile) \
        .filter(user_profile_model.UserProfile.user_id == user_id).first()

    if db_user_profile:
        db_user_profile.profile_picture = profile_picture
        db.commit()
        db.refresh(db_user_profile)

    return db_user_profile

def update_user_profile(db: Session, user_profile: user_profile_schema.UserProfileInDB):
    """
    Utility function to update the user's profile information. User must have a user profile.

    Parameters
    ----------
    db: Session
        a database session
    user_profile: schemas.user_profile_schema.UserProfileInDB
        a pydantic model representing a user's profile in the database

    Returns
    -------
    models.user_profile_model.UserProfile
        sql alchemy object representing the updated user profile
    """

    current_user_profile = db.query(user_profile_model.UserProfile) \
        .filter(user_profile_model.UserProfile.user_id == user_profile.user_id).first()
    if current_user_profile:
        current_user_profile.first_name = user_profile.first_name
        current_user_profile.last_name = user_profile.last_name
        db.commit()
        db.refresh(current_user_profile)
        return current_user_profile