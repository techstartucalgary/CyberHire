from fastapi import APIRouter, Depends, HTTPException, status, Path, File, Response
from sqlalchemy.orm import Session
from ..schemas import user_profile_schema
from ..models import user_profile_model, user_model
from ..database import SessionLocal
from .. import dependencies
from ..crud import user_profile_crud, user_crud

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

    return user_profile_crud.get_user_profiles(db)

@router.get(
    "/users/profile/me",
    response_model=user_profile_schema.UserProfile,
    status_code=status.HTTP_200_OK,
    tags=["UserProfile"],
    summary="Get the current user's profile information.",
    description="Get the current logged in user's profile information, including " \
        "first name, last name, profile picture as bytes string, resume " \
        "as bytes string, and a list of skills.",
    response_description="The current user's profile information."
)
def get_user_profile_me(
    db: Session = Depends(dependencies.get_db),
    current_user: user_model.User = Depends(dependencies.get_current_user)
):
    # Ignore the type error from pylance
    return user_profile_crud.get_user_profile_by_id(db, current_user.id)

@router.get(
    "/users/profile/{username}",
    response_model=user_profile_schema.UserProfile,
    status_code=status.HTTP_200_OK,
    tags=["UserProfile"],
    summary="Get a user's profile information.",
    description="Get a current user's profile information, including " \
        "first name, last name, profile picture as bytes string, resume " \
        "as bytes string, and a list of skills.",
    response_description="A user's profile information."
)
def get_user_profile(
    db: Session = Depends(dependencies.get_db),
    username: str = Path()
):
    user = user_crud.get_user_by_username(db, username)
    if not user:
        raise HTTPException(status_code=400, detail="Username does not exist.")
    return user_profile_crud.get_user_profile_by_id(db, user.id)

@router.post(
    "/users/profile/",
    response_model=user_profile_schema.UserProfile,
    status_code=status.HTTP_201_CREATED,
    tags=["UserProfile"],
    summary="Create a new user profile.",
    description="Create a new user profile with all information, including " \
        "first name, last name, profile picture as bytes string, and resume " \
        "as bytes string.",
    response_description="The newly created user's profile information."
)
def create_user_profile(
    *,
    db: Session = Depends(dependencies.get_db),
    current_user: user_model.User = Depends(dependencies.get_current_user),
    user_profile: user_profile_schema.UserProfileCreate
):
    current_user_profile = user_profile_crud.get_user_profile_by_id(db, current_user.id)
    if current_user_profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User profile already exists."
        )
    return user_profile_crud.create_user_profile(db, current_user.id, user_profile)
    
@router.patch(
    "/users/profile/resume",
    responses = {
        200: {
            "content": {"application/pdf": {}}
        }
    },
    status_code=status.HTTP_200_OK,
    tags=["UserProfile"],
    summary="Update a user's resume.",
    description="Update a user's resume as bytes string.",
    response_description="The newly updated user's resume.",
    response_class=Response
)
def update_user_resume(
    db: Session = Depends(dependencies.get_db),
    current_user: user_model.User = Depends(dependencies.get_current_user),
    resume: bytes | None = File(default=None)
):
    database_user : user_profile_model.UserProfile = user_profile_crud.update_user_resume(
        db,
        current_user.id,
        resume
    )
    file = database_user.resume
    return Response(
        content=file,
        media_type="application/pdf",
        headers={
            "content-disposition": f"attachment; filename={current_user.username}_resume.pdf"
        }
    )

@router.patch(
    "/users/profile/profile_picture",
    responses = {
        200: {
            "content": {"image/jpg": {}}
        }
    },
    status_code=status.HTTP_200_OK,
    tags=["UserProfile"],
    summary="Update a user's profile picture",
    description="Update a user's profile picture as a bytes string.",
    response_description="The newly updated user's profile picture.",
    response_class=Response
)
def update_user_profile_picture(
    db: Session = Depends(dependencies.get_db),
    current_user: user_model.User = Depends(dependencies.get_current_user),
    profile_picture: bytes | None = File(default=None)
):
    database_user : user_profile_model.UserProfile = user_profile_crud.update_user_profile_picture(
        db,
        current_user.id,
        profile_picture
    )

    file = database_user.profile_picture
    return Response(
        content=file,
        media_type="image/jpg",
        headers={
            "content-disposition": f"attachment; filename={current_user.username}_profile_picture.jpg"
        }
    )
