from fastapi import APIRouter, Depends, status, HTTPException, Path

from sqlalchemy.orm import Session

from .. import dependencies
from ..schemas import job_schema
from ..models import user_model
from ..crud import user_profile_crud, job_crud, job_matching_crud

router = APIRouter()

@router.get(
    "/job_matching/",
    response_model=list[job_schema.Job],
    status_code=status.HTTP_200_OK,
    tags=["Job Matching"],
    summary="GET route to obtain the top ten jobs for an applicant.",
    description="The applicant must have created a user profile and listed " \
        "their top skills. If the applicant has not listed their top skills " \
        "then random jobs will be returned. The jobs are returned in order of best " \
        "match to worst match. Jobs that an applicant have applied for are not returned.",
    response_description="The applicants top ten job matches."
)
def get_job_matching(db: Session=Depends(dependencies.get_db),
                     applicant: user_model.User=Depends(dependencies.get_current_applicant_user)):
    """
    GET route to obtain a list of the top ten jobs that match the applicant's skills from the
    database. The jobs are matched based on the number of skills that match between a job and an
    applicant. The jobs are returned in order of best match to worst match and only jobs that
    the applicant have not applied to are returned.

    Parameters
    ----------
    db: Session
        a database session
    applicant: user_model.User
        a sqlalchemy user object that represents the current authorized applicant

    Returns
    -------
    list[job_schema.Job]
        a list of pydantic models representing the best matched jobs for the applicant
    """
    
    # Check if they have a user profile
    dependencies.user_profile_exists(db, applicant.id)

    # Check if they have any skills
    applicant_profile = user_profile_crud.get_user_profile_by_id(db, applicant.id)

    # If not then return 10 random jobs
    # If yes then return top 10 matches
    if applicant_profile is not None:
        if not len(applicant_profile.skills) > 0:
            return job_crud.get_all_jobs(db)
        else:
            return job_matching_crud.get_job_matching(db, applicant.id)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User profile for applicant {applicant.id} does not exist.")
