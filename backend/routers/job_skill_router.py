from sqlalchemy.orm import Session

from fastapi import APIRouter, Depends, Path, HTTPException
from fastapi import status

from ..schemas import skill_schema, job_schema
from .. import dependencies
from ..crud import job_crud, skill_crud
from ..models import user_model

router = APIRouter()

# Get route to get all the skills for a job
@router.get(
    "/jobs/skills/{job_id}",
    response_model=list[skill_schema.Skill],
    status_code=status.HTTP_200_OK,
    tags=["Job", "Skill"],
    summary="GET route to get all the skills for a job.",
    description="Return all the skills for the job id, " \
        "or an empty list if it doesn't have any.",
    response_description="A list of all the skills required of the job."
)
def get_job_skills(db: Session=Depends(dependencies.get_db), job_id: int=Path()):
    """
    GET route to obtain all the skills related to a job

    Parameters
    ----------
    db: Session
        a database session

    Returns
    -------
    list[skill_schema.Skill]
        A list of pydantic models for skills related to the job
    """

    # Check if the job exists
    job = job_crud.get_job_by_id(db, job_id)

    if job is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Job with job id {job_id} not found.")

    # Return their skills
    return job.skills

# Post route to replace all the skills for a job
@router.post(
    "/jobs/skills/{job_id}",
    response_model=job_schema.Job,
    status_code=status.HTTP_201_CREATED,
    tags=["Job", "Skill"],
    summary="Update the skills for a job.",
    description="This route will remove all of the job's current required skills " \
                "and replace them with the list of the skills provided.",
    response_description="The updated job in the database with new required skills."
)
def create_skills_for_job(*,
                          db: Session=Depends(dependencies.get_db),
                          job_id: int=Path(),
                          recruiter: user_model.User=Depends(dependencies.get_current_recruiter_user),
                          new_skills: list[skill_schema.SkillCreate] | None):
    """
    POST route to replace all of a jobs related skills

    Parameters
    ----------
    db: Session
        a database sesion
    job_id: int
        The unique id of the job
    recruiter: user_model.User
        a sqlalchemy object representing the current authenticated recruiter user
    new_skills: list[skill_schema.SkillCreate] | None
        a list of pydantic models representing the new skills for the job, or None to only
        remove previous skills without replacing

    Returns
    -------
    job_schema.Job
        a pydantic model for a job with the newly updated skills information embedded
    """

    # Check if the job exists and it belongs to the recruiter
    job = job_crud.get_job_by_id(db, job_id)

    if job is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Job with job id {job_id} not found.")

    if job.user_profile_id != recruiter.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"Recruiter with id {recruiter.id} is not authorized to " \
                                    "update this job.")

    # Check if all skills provided exist in the database
    new_skills_in_db = []
    if new_skills is not None:
        for skill in new_skills:
            skill_model = skill_crud.get_skill_by_name(db, skill.skill)
            if skill_model is not None:
                new_skills_in_db.append(skill_model)
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail=f"Skill with name {skill.skill} not found in database.")

    # Delete the skills for the current job
    skill_crud.delete_all_job_skills(db, job_id)

    # Create new skills for the current job
    for skill in new_skills_in_db:
        skill_crud.create_job_skill(db, job.id, skill.id)

    # Return the updated job
    return job_crud.get_job_by_id(db, job_id)
