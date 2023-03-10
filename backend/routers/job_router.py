from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status, Path, HTTPException
from .. import dependencies
from .. models import user_model
from ..schemas import job_schema
from ..crud import job_crud

# Router for job information
router = APIRouter()

# GET /jobs get all jobs

@router.get(
    "/jobs",
    response_model=list[job_schema.Job] | None,
    status_code=status.HTTP_200_OK,
    tags=["Job"],
    summary="GET route to obtain information for all jobs posted.",
    description="Return a list of all jobs posted, including job title, " \
        "job description, job location, salary range, skills required, and " \
        "profile of the job poster.",
    response_description="A list of all jobs posted."
)
def get_all_jobs(db: Session=Depends(dependencies.get_db)):

    return job_crud.get_all_jobs(db)

# GET /jobs/{job_id} get a specific job
@router.get(
    "/jobs/{job_id}",
    response_model=job_schema.Job,
    status_code=status.HTTP_200_OK,
    tags=["Job"],
    summary="GET route to obtain information for a specific job posted.",
    description="Return information for a specific job posted, including job title, " \
        "job description, job location, salary range, skills required, and " \
        "profile of the job poster.",
    response_description="A specific job posted."
)
def get_a_job(db: Session=Depends(dependencies.get_db), job_id: int=Path()):

    job = job_crud.get_job_by_id(db, job_id)
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Job does not exist with id {job_id}")
    return job

# GET /jobs/me get a list of all a recruiters job postings
@router.get(
    "/jobs/me",
    response_model=job_schema.Job,
    status_code=status.HTTP_200_OK,
    tags=["Job"],
    summary="GET route to obtain a list of all the current recruiter's job postings.",
    description="Return information for all of the current recruiter's job postings. " \
        "Includes information such as job title, job description, job location, " \
        " salary range, skills required, and profile of the job poster.",
    response_description="A list of all the current recruter's job postings."
)
def get_all_recruiter_jobs(db: Session=Depends(dependencies.get_db),
        recruiter: user_model.User=Depends(dependencies.get_current_recruiter_user)):

    jobs = job_crud.get_jobs_by_user_profile_id(db, recruiter.id)

    if len(jobs) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Recruiter {recruiter.id} has no jobs posted.")    

    return jobs

# POST /jobs post a new job
@router.post(
    "/jobs",
    response_model=job_schema.Job,
    status_code=status.HTTP_201_CREATED,
    tags=["Job"],
    summary="POST route to post a new job for the current recruiter.",
    description="POST a new job for the current recruiter. The recruiter " \
        "must provide the job title, a description, and the location of the job. " \
        "Salary is optional if not provided.",
    response_description="The newly created job posting in the database."
)
def create_job(*, db: Session=Depends(dependencies.get_db),
               recruiter: user_model.User=Depends(dependencies.get_current_recruiter_user),
               new_job: job_schema.JobCreate):
    
    # Check if user profile exists
    dependencies.user_profile_exists(db, recruiter.id)

    # Create the job
    new_job_db = job_crud.create_job(db, recruiter.id, new_job)

    return new_job_db

# PATCH /jobs/{job_id} update a job
@router.patch(
    "/jobs/{job_id}",
    response_model=job_schema.Job,
    status_code=status.HTTP_200_OK,
    tags=["Job"],
    summary="PATCH route to update an existing recruiter's posted job.",
    description="PATCH route to update a job posted by the current recruiter. " \
        "Recruiters can only update their own jobs. All information is optional, " \
        "if a value is not provided for a field, the current value of the field " \
        "in the database remains unchanged.",
    response_description="The job with the updated information."
)
def update_job(*, db: Session=Depends(dependencies.get_db),
               recruiter: user_model.User=Depends(dependencies.get_current_recruiter_user),
               new_job: job_schema.JobPatch,
               job_id: int = Path()):
    
    # Check if the job exists and the recruiter posted the job
    job_in_db_model = job_crud.get_job_by_id(db, job_id)

    if job_in_db_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Job with id: {job_id} does not exist.")
    
    if job_in_db_model.user_profile_id != recruiter.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"Recruiter with id: {recruiter.id} is not authorized to " \
                                "update this job.")

    # Convert the job from the database to a pydantic model
    job_in_db_schema = job_schema.JobInDb(
        title=job_in_db_model.title,
        description=job_in_db_model.description,
        location=job_in_db_model.location,
        min_salary=job_in_db_model.min_salary,
        max_salary=job_in_db_model.max_salary,
        id=job_in_db_model.id,
        user_profile_id=job_in_db_model.user_profile_id
    )

    # Update the pydantic model with the new job information
    job_in_db_schema.copy(update=new_job.dict())

    # Save the new job information to the database
    updated_job = job_crud.update_job(db, job_in_db_schema)

    # Return the new job information
    return updated_job

# DELETE /jobs/{job_id} delete a job



# POST /jobs/{job_id}/skills 