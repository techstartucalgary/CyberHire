from fastapi import APIRouter, Depends, status, HTTPException, Path

from sqlalchemy.orm import Session

from ..schemas import user_profile_job_schema
from ..models import user_profile_job_model, user_model, application_status_model
from .. import dependencies
from ..crud import user_profile_job_crud, job_crud

router = APIRouter()

# GET /applications/me get all an applicant's applications
@router.get(
    "/applications/me",
    response_model=list[user_profile_job_schema.UserProfileJob],
    status_code=status.HTTP_200_OK,
    tags=["Application"],
    summary="GET route to obtain all an applicant users applications in the database.",
    description="Return a list of all an applicant users applications in the database, " \
        "including the application status, the applicants information, the job information, " \
        "date the application was submitted, reviewed and offer was sent or rejected. " \
        " Query for applications in a specific status by specifying query parameter q.",
    response_description="A list of all an applicant users applications."
)
def get_applicants_applications(*,
                                db: Session = Depends(dependencies.get_db),
                                applicant: user_model.User = Depends(dependencies.get_current_user),
                                q: application_status_model.ApplicationStatusEnum | None = None):

    # check if query parameter was specified
    if q is None:
        # if not query the database for all the applications with the applicant's id
        applications = user_profile_job_crud.get_applications_by_user_id(db, applicant.id)
    else:
        # if yes query the database for all applications with the applicant's id and 
        # filter by query param
        applications = user_profile_job_crud \
            .get_applications_by_user_id_and_status(db, applicant.id, q)

    if len(applications) == 0:
        if q is None:
            detail = f"No applications were found for user {applicant.id}."
        else:
            detail = f"No applications were found for user {applicant.id} with status {q.name}."
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=detail)

    return applications

# GET /applications/me/{jobId} get an applicant’s application
@router.get(
    "/applications/me/{job_id}",
    response_model=user_profile_job_schema.UserProfileJob,
    status_code=status.HTTP_200_OK,
    tags=["Application"],
    summary="GET route to obtain an applicant user's application " \
        "in the database for a specific job.",
    description="Return a applicant user's application in the database, including the status, " \
        "the applicant's information, the job information, the data the application " \
        "was submitted, reviewed and offer was sent or rejected.",
    response_description="The application for the specified job."
)
def get_applicants_application_by_job_id(db: Session = Depends(dependencies.get_db),
                                         applicant: user_model.User = Depends(dependencies.get_current_applicant_user),
                                         job_id = Path()):

    # query the database for the application
    application = user_profile_job_crud \
        .get_application_by_user_id_and_job_id(db, applicant.id, job_id)

    # check if an application was found
    if application is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Application for job {job_id} not found for applicant {applicant.id}.")

    return application

# GET /applications/{jobId} get all applicants for a job
@router.get(
    "/applications/{job_id}",
    response_model=list[user_profile_job_schema.UserProfileJob],
    status_code=status.HTTP_200_OK,
    tags=["Application"],
    summary="GET route to obtain all applications for a specific job for a recruiter.",
    description="The recruiter must own the job to get applications for it. Returns a list of " \
        "applications for the specified job.",
    response_description="The applications for the specified job."
)
def get_applications_by_job_id(db: Session = Depends(dependencies.get_db),
                               recruiter: user_model.User = Depends(dependencies.get_current_recruiter_user),
                               job_id: int = Path(),
                               q: application_status_model.ApplicationStatusEnum | None = None):

    # check if the recruiter owners the job
    job = job_crud.get_job_by_id(db, job_id)

    if job is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Could not find job with id {job_id}.")
    if job.user_profile_id != recruiter.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"Recruiter is not authorized to view applications for job {job_id}.")

    # check if the query parameter was specified
    if q is None:
        # if not get all the applications for the job
        applications = user_profile_job_crud.get_applications_by_job_id(db, job_id)
    else:
        # if yes get all the applications for the job and filter by status
        applications = user_profile_job_crud.get_applications_by_job_id_and_status(db, job_id, q)

    # check if there were any applications
    if len(applications) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="No applications found for job {job_id}.")

    return applications

# POST /applications create a new application
@router.post(
    "/applications/{job_id}",
    response_model=user_profile_job_schema.UserProfileJob,
    status_code=status.HTTP_201_CREATED,
    tags=["Application"],
    summary="POST route for an applicant user to create a new application for a specific job.",
    description="The applicant must have a user profile to submit applications for " \
        "a job. The applicant cannot submit an application for the same job more than once.",
    response_description="The new application for the specified job."
)
def create_applicant_application(db: Session = Depends(dependencies.get_db),
                                 job_id: int = Path(),
                                 applicant: user_model.User = Depends(dependencies.get_current_applicant_user)):

    # check if the job exists
    job = job_crud.get_job_by_id(db, job_id)

    if job is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Job with id {job_id} does not exist.")

    # check if the applicant has a database profile
    dependencies.user_profile_exists(db, applicant.id)

    # check if the application already exists
    application = user_profile_job_crud.get_application_by_user_id_and_job_id(db, applicant.id, job_id)

    if application is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Applicant {applicant.id} already applied to job {job_id}.")

    # create a new application
    return user_profile_job_crud.create_applicant_application(db, applicant.id, job_id)

# DELETE /applications/{job_id} delete an application
@router.delete(
    "/applications/me/{job_id}",
    status_code=status.HTTP_200_OK,
    tags=["Application"],
    summary="DELETE route for an applicant to delete an application for a specific job.",
    description="Delete the current user's application for a specific job from the database.",
    response_description="The deleted user's application."
)
def delete_applicant_application(db: Session = Depends(dependencies.get_db),
                                 job_id: int = Path(),
                                 applicant: user_model.User = Depends(dependencies.get_current_applicant_user)):

    # check if the application exists
    application = user_profile_job_crud.get_application_by_user_id_and_job_id(db, applicant.id, job_id)

    if application is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Application for applicant {applicant.id} and job {job_id} not found.")

    # delete the application
    return f"Deleted application for job {job_id} for applicant {applicant.id}."


# PATCH /applications/{job_id}_{applicant_id}/review change status to under review
# @router.patch(
#     "/applications/review/"
# )

# PATCH /applications/{job_id}_{applicant_id}/further_screening 

# PATCH /applications/{job_id}_{applicant_id}/offer change status to offer sent

# PATCH /applications/{job_id}_{applicant_id}/rejected change status to rejected