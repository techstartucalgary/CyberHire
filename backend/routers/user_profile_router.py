from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..schemas import user_profile_schema
from ..models import user_profile_model
from ..database import SessionLocal
from .. import dependencies
from ..crud import user_profile_crud

router = APIRouter()

@router.get(
    "/users/profile",
    response_model=list[user_profile_schema.UserProfile],
    status_code=status.HTTP_200_OK,
    tags=["UserProfile"],
    summary="Get route to obtain all user's profiles.",
    description="Return a list of all user's profiles, including " \
        "first name, last name, profile picture as bytes string, resume as " \
        "bytes string, and a list of skills.",
    response_description="A list of all user's profiles."
)
def get_user_profiles(db: Session = Depends(dependencies.get_db)):
    print(user_profile_crud.get_user_profiles(db))
    return user_profile_crud.get_user_profiles(db)

@router.get(
    "/users/profile/me",
    response_model=user_profile_schema.UserProfile,
    status_code=status.HTTP_200_OK,
    tags=["UserProfile"],
    summary="Get the current user's profile information.",
    description="Get the current logged in user's profile information, including " \
        "first name, last name, profile picture as bytes string, resume " \
        "as bytes string, and a list of skills",
    response_description="The current user's profile information."
)
def get_user_profile_me(
    db: Session = Depends(dependencies.get_db),
    current_user = Depends(dependencies.get_current_user)
):
    return user_profile_crud.get_user_profile_by_id(db, current_user.id)

