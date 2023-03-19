from sqlalchemy.orm import Session

from fastapi import APIRouter, Depends, status

from ..schemas import user_profile_schema, skill_schema
from ..models import user_model
from .. import dependencies
from ..crud import user_profile_crud, skill_crud

router = APIRouter()

@router.get(
    "/users/profile/me/skills",
    response_model=list[skill_schema.Skill],
    status_code=status.HTTP_200_OK,
    tags=["UserProfile", "Skill"],
    summary="Get all the skills in the current user's profile.",
    description="Return all the skills of the current authenticated user's profile, " \
        "or an empty list if they don't have any.",
    response_description="A list of all the skills of the current authenticated user."
    )
def get_user_profile_skills(db: Session = Depends(dependencies.get_db),
                current_user: user_model.User = Depends(dependencies.get_current_user)):
    """
    Get route to obtain a list of skills associated with the current authenticated user.

    Parameters
    ----------
    db: Session
        a database session
    current_user: models.user_model.User
        a sqlalchemy user object representing the current authenticated user

    Returns
    -------
    list[schemas.skill_schema.Skill]
        a list of pydantic Skill objects representing the current user's skills
    """
    dependencies.user_profile_exists(db, current_user.id)
    return skill_crud.get_skills_by_user_id(db, current_user.id)


@router.post(
    "/users/profile/me/skills",
    response_model=user_profile_schema.UserProfile,
    status_code=status.HTTP_201_CREATED,
    tags=["UserProfile", "Skill"],
    summary="Update the current authenticated user's skills.",
    description="This route will remove all of the current user's skills " \
        "in the database and create new ones " \
        "with the list of skills provided.",
    response_description="The updated user's profile."
    )
def create_skills_for_user_profile(*, db: Session = Depends(dependencies.get_db),
                current_user: user_model.User = Depends(dependencies.get_current_user),
                skills: list[skill_schema.SkillCreate] | None):
    """
    A POST route to update the skills of the current authenticated user. Useful for
    deleting all a user's skills, updating the user's skills with a new set, or
    adding new skills to the current set.

    Parameters
    ----------
    db: Session
        a database session
    current_user: models.user_model.User
        a sqlalchemy user object representing the current authenticated user
    skills: list[schemas.skill_schema.SkillCreate] | None
        a list of pydantic skill objects for associating new skills with the authenticated user

    Returns
    -------
    schemas.user_profile_schema.UserProfile
        The current user's profile with updated skills
    """
    # get the current user's id
    current_user_id = current_user.id
    dependencies.user_profile_exists(db, current_user_id)
    # delete the current user's skills
    skill_crud.delete_all_user_profile_skill(db, current_user_id)
    # get the skill ids from all skill names
    if skills is not None:
        for new_skill in skills:
            # add a row to the user_profile_skill model for each of the id's
            db_skill = skill_crud.get_skill_by_name(db, new_skill.skill)
            if db_skill is not None:
                skill_crud.create_user_profile_skill(db, current_user_id, db_skill.id)

    return user_profile_crud.get_user_profile_by_id(db, current_user_id)
