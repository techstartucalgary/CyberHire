from fastapi import APIRouter, Depends, HTTPException, status, Path, File, Response
from sqlalchemy.orm import Session
from ..schemas import user_profile_schema
from ..models import user_profile_model, user_model
from .. import dependencies
from ..crud import user_profile_crud, user_crud

router = APIRouter()

@router.get(
    "/users/profile",
    response_model=list[user_profile_schema.UserProfile] | None,
    status_code=status.HTTP_200_OK,
    tags=["UserProfile"],
    summary="Get route to obtain all user's profiles.",
    description="Return a list of all user's profiles, including " \
        "first name, last name, profile picture as bytes string, resume as " \
        "bytes string, and a list of skills.",
    response_description="A list of all user's profiles."
)
def get_user_profiles(db: Session = Depends(dependencies.get_db)):
    """
    A GET route to obtain all user's profiles from the database.

    Parameters
    ----------
    db: Session
        a database connection

    Returns
    -------
    list[schemas.user_profile_schema.UserProfile] | None
        A list of pydantic models for user profiles, or none if there are no user profiles.
    """

    return user_profile_crud.get_user_profiles(db)

@router.get(
    "/users/profile/me",
    response_model=user_profile_schema.UserProfile | None,
    status_code=status.HTTP_200_OK,
    tags=["UserProfile"],
    summary="Get the current user's profile information.",
    description="Get the current logged in user's profile information, including " \
        "first name, last name, profile picture as bytes string, resume " \
        "as bytes string, and a list of skills.",
    response_description="The current user's profile information."
)
def get_user_profile_me(db: Session = Depends(dependencies.get_db),
        current_user: user_model.User = Depends(dependencies.get_current_user)):
    """
    A GET route to obtain the current authenticated user's profile information.

    Parameters
    ----------
    db: Session
        a database session
    current_user: models.user_model.User
        a sqlalchemy object representing the current authenticated user

    Returns
    -------
    schemas.user_profile_schema.UserProfile
        The current user's profile information
    """
    dependencies.user_profile_exists(db, current_user.id)
    # Ignore the type error from pylance
    return user_profile_crud.get_user_profile_by_id(db, current_user.id)

@router.get(
    "/users/profile/me/profile_picture",
    status_code=status.HTTP_200_OK,
    tags=["UserProfile"],
    summary="Retrieve the current user's profile picture from the database.",
    description="Retrieve the current user's profile picture from the database as a jpg file.",
    response_description="The current user's profile picture."
)
def get_user_profile_picture_me(
    db: Session = Depends(dependencies.get_db),
    current_user: user_model.User = Depends(dependencies.get_current_user)
):
    """
    A GET route to obtain the current authenticated user's profile picture.

    Parameters
    ----------
    db: Session
        a database session
    current_user: models.user_model.User
        a sqlalchemy pbject representing the current authenticated user

    Returns
    -------
    fastapi.Response
        a response with the profile picture
    """
    dependencies.user_profile_exists(db, current_user.id)
    database_user_profile : user_profile_model.UserProfile = user_profile_crud.get_user_profile_by_id(
        db,
        current_user.id
    )

    if database_user_profile is not None:
        file = database_user_profile.profile_picture

        if file is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User {current_user.id} does not have a profile picture in the database."
            )

        return Response(
            content=file,
            media_type="image/jpg",
            headers={
                "content-disposition": f"attachment; \
                    filename={current_user.username}_profile_picture.jpg"
            }
        )

@router.get(
    "/users/profile/me/resume",
    status_code=status.HTTP_200_OK,
    tags=["UserProfile"],
    summary="Retrieve the current user's resume from the database.",
    description="Retrieve the current user's resume from the database as a pdf file.",
    response_description="The current user's resume."
)
def get_user_resume_me(
    db: Session = Depends(dependencies.get_db),
    current_user: user_model.User = Depends(dependencies.get_current_user)
):
    """
    A GET route to obtain the current authenticated user's resume.

    Parameters
    ----------
    db: Session
        a database session
    current_user: models.user_model.User
        a sqlalchemy pbject representing the current authenticated user

    Returns
    -------
    fastapi.Response
        a response with the resume
    """
    dependencies.user_profile_exists(db, current_user.id)
    database_user_profile : user_profile_model.UserProfile = user_profile_crud.get_user_profile_by_id(
        db,
        current_user.id
    )

    if database_user_profile is not None:
        file = database_user_profile.resume

        if file is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User {current_user.id} does not have a resume in the database."
            )

        return Response(content=file, media_type="application/pdf",
            headers={
                "content-disposition": f"attachment; \
                    filename={current_user.username}_resume.pdf"
            }
        )

@router.get(
    "/users/profile/{username}",
    response_model=user_profile_schema.UserProfile | None,
    status_code=status.HTTP_200_OK,
    tags=["UserProfile"],
    summary="Get a user's profile information.",
    description="Get a current user's profile information, including " \
        "first name, last name, profile picture as bytes string, resume " \
        "as bytes string, and a list of skills.",
    response_description="A user's profile information."
)
def get_user_profile(db: Session = Depends(dependencies.get_db), username: str = Path()):
    """
    Parameters
    ----------
    db: Session
        a database session
    username: str
        the user's username

    Returns
    -------
    schemas.user_profile_schema.UserProfile
    """
    user = user_crud.get_user_by_username(db, username)
    if not user:
        raise HTTPException(status_code=400, detail="Username does not exist.")
    dependencies.user_profile_exists(db, user.id)
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
def create_user_profile(*, db: Session = Depends(dependencies.get_db),
        current_user: user_model.User = Depends(dependencies.get_current_user),
        user_profile: user_profile_schema.UserProfileCreate
        ):
    """
    A POST route to create a new user profile for the current authenticated user.

    Parameters
    ----------
    db: Session
        a database session
    current_user: models.user_model.User
        a sqlalchemy User object representing the current authenticated user
    user_profile: schemas.user_profile_schema.UserProfileCreate
        a pydantic model representing the current authenticated user's profile information

    Returns
    -------
    schemas.user_profile_schema.UserProfile
        the current authenticated user's new profile information
    """
    current_user_profile = user_profile_crud.get_user_profile_by_id(db, current_user.id)
    if current_user_profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User profile already exists."
        )
    return user_profile_crud.create_user_profile(db, current_user.id, user_profile)

@router.delete(
    "/users/profile/me",
    response_model=user_profile_schema.UserProfile,
    status_code=status.HTTP_200_OK,
    tags=["UserProfile"],
    summary="Delete the current user's profile from the database.",
    description="Delete the current user's profile from the database, " \
        "inlcuding their name, profile picture, resume, and skills.",
    response_description="The deleted user's profile."
)
def delete_user_profile_me(db: Session = Depends(dependencies.get_db),
        current_user: user_model.User = Depends(dependencies.get_current_user)):
    """
    A DELETE route to delete the current authenticated user's profile.

    Parameters
    ----------
    db: Session
        a database session
    current_user:models.user_model.User
         a sqlalchemy User object representing the current authenticated user

    Returns
    -------
    schemas.user_profile_schema.UserProfile
        a pydnatic user profile object representing the deleted user profile
    """

    dependencies.user_profile_exists(db, current_user.id)
    return user_profile_crud.delete_user_profile(db, current_user.id)

@router.patch(
    "/users/profile/resume",
    responses = {
        200: {
            "content": {"application/pdf": {}}
        }
    },
    status_code=status.HTTP_200_OK,
    tags=["UserProfile"],
    summary="Update the current user's resume.",
    description="Update the curent user's resume, resume must be a pdf. None is permitted to " \
        "erase their resume from the database. User must first create a user profile to update " \
        "ther resume.",
    response_description="The newly updated user's resume.",
    response_class=Response
)
def update_user_resume(db: Session = Depends(dependencies.get_db),
        current_user: user_model.User = Depends(dependencies.get_current_user),
        resume: bytes | None = File(default=None)):
    """
    A PATCH route to replace a user's resume in the user_profile table in
    the database. None is acceptable to erase the user's resume from the database.

    Parameters
    ----------
    db: Session
        a database session
    current_user: models.user_model.User
        a sqlalchemy user object representing the current authenticated user
    resume: bytes | None
        A pdf resume or None

    Returns
    -------
    fastapi.Response
        a response with the newly updated resume
    """
    dependencies.user_profile_exists(db, current_user.id)
    database_user : user_profile_model.UserProfile = user_profile_crud.update_user_resume(
        db, current_user.id, resume)
    file = database_user.resume
    return Response(content=file, media_type="application/pdf",
        headers={
            "content-disposition": f"attachment; \
                filename={current_user.username}_resume.pdf"
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
    summary="Update the current user's profile picture.",
    description="Update the current user's profile picture, profile picture must be a jpg. " \
        "None is permitted to erase the user's profile picture. User must first create a " \
        "user profile to update their profile picture.",
    response_description="The newly updated user's profile picture.",
    response_class=Response
)
def update_user_profile_picture(db: Session = Depends(dependencies.get_db),
        current_user: user_model.User = Depends(dependencies.get_current_user),
        profile_picture: bytes | None = File(default=None)):
    """
    A PATCH route to replace a user's profile picture in the user_profile table
    in the database. None is acceptable to erase the user's profile picture from the database.

    Parameters
    ----------
    db: Session
        a database session
    current_user: models.user_model.User
        a sqlalchemy user object representing the current authenticated user
    profile_picture: bytes | None
        a jpg profile picture or None
    """

    dependencies.user_profile_exists(db, current_user.id)
    database_user_profile : user_profile_model.UserProfile = user_profile_crud.update_user_profile_picture(
        db, current_user.id, profile_picture)
    
    if database_user_profile is not None:
        file = database_user_profile.profile_picture
        return Response(
            content=file,
            media_type="image/jpg",
            headers={
                "content-disposition": f"attachment; \
                    filename={current_user.username}_profile_picture.jpg"
            }
        )

@router.patch(
    "/users/profile/me",
    response_model=user_profile_schema.UserProfile,
    status_code=status.HTTP_200_OK,
    tags=["UserProfile"],
    summary="Update the current authenticated user's profile information.",
    description="Update the current authenticated user's profile information.",
    response_description="The current authenticated user's updated profile information and skills."
)
def update_user_profile(*, db: Session = Depends(dependencies.get_db),
        current_user: user_model.User = Depends(dependencies.get_current_user),
        new_user_data: user_profile_schema.UserProfilePatch):
    """
    A PATCH route to update the current authenticated user's profile information.
    Only the information provided by the user is updated.
    For example, if the user only passes in a new first name, then only the first name is updated.

    Parameters
    ----------
    db: Session
        a database session
    current_user: models.user_model.User
        a sqlalchemy User object representing the current authenticated user
    new_user_data: schemas.user_profile_schema.UserProfilePatch
        a pydantic model representing the current user's new profile information. If no value
        is provided for an attribute, then those attributes are not updated.

    Returns
    -------
    schemas.user_profile_schema.UserProfile
        The current user's new profile information
    """
    dependencies.user_profile_exists(db, current_user.id)
    current_user_data: user_profile_model.UserProfile = user_profile_crud.get_user_profile_by_id(db, current_user.id)

    current_user_profile_model = user_profile_schema.UserProfileInDB(
        user_id=current_user_data.user_id,
        first_name=current_user_data.first_name,
        last_name=current_user_data.last_name
    )

    update_data = new_user_data.dict(exclude_unset=True)
    updated_user_profile = current_user_profile_model.copy(update=update_data)

    return user_profile_crud.update_user_profile(db, updated_user_profile)

