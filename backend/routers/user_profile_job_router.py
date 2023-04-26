from fastapi import APIRouter, Depends, status, HTTPException, Path, Body

from sqlalchemy.orm import Session

from ..schemas import user_profile_job_schema
from ..models import user_model, application_status_model
from .. import dependencies
from ..crud import user_profile_job_crud, job_crud, application_status_crud

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
        "Query for applications in a specific status by specifying query parameter q.",
    response_description="A list of all an applicant users applications."
)
def get_applicants_applications(*,
                                db: Session = Depends(dependencies.get_db),
                                applicant: user_model.User = Depends(dependencies.get_current_applicant_user),
                                q: application_status_model.ApplicationStatusEnum | None = None):
    """
    GET route to to obtain the current authenticated applicant user's list of applications for all
    jobs from the datbase. Query for applications in a specific status by specifying query parameter q.
    An error is returned if no applications were found.

    Parameters
    ----------
    db: Session
        a database session
    applicant: user_model.User
        a sqlalchemy object representing the current authenticated applicant user
    q: application_status_model.ApplicationStatusEnum | None
        optional parameter to specify the application status type to query for

    Returns
    -------
    list[user_profile_job_schema.UserProfileJob]
        a list of pydantic models for applications created for the current applicant
    """

    # check if query parameter was specified
    if q is None:
        # if not query the database for all the applications with the applicant's id
        applications = user_profile_job_crud.get_applications_by_user_id(db, applicant.id)
    else:
        # if yes query the database for all applications with the applicant's id and 
        # filter by query param
        application_status = application_status_crud.get_application_status_by_name(db, q.value)
        applications = user_profile_job_crud \
            .get_applications_by_user_id_and_status(db, applicant.id, application_status.id)

    if len(applications) == 0:
        if q is None:
            detail = f"No applications were found for user {applicant.id}."
        else:
            detail = f"No applications were found for user {applicant.id} with status {q.value}."
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
                                         job_id: int = Path()):
    """
    GET route to obtain the current authenticated applicant user's application for a specific job
    from the database. An error is returned if no applications are found for the job.

    Parameters
    ----------
    db: Session
        a database session]
    applicant: user_model.User
        a sqlalchemy object representing the current authenticated applicant user
    job_id: int
        the job's unique identifier in the database

    Returns
    -------
    user_profile_job_schema.UserProfileJob
        a pydantic model for a application created for the specified job
    """

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
    """
    GET route for a recruiter to obtain all applications for a specific job. The recruiter
    must own the job to get applications for it. If the recruiter does not own the job, an
    error will be returned.

    Parameters
    ----------
    db: Session
        a database session
    recruiter: user_model.User
        a sql alchemy object representing the current authenticated recruiter user
    job_id: int
        the job's unique identifier in the database
    q: application_status_model.ApplicationStatusEnum | None
        optional query parameter to filter the applications returned by their
        application status type

    Returns
    -------
    list[user_profile_job_schema.UserProfileJob]
        a list of all applications for the specified job
    """

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
        application_status = application_status_crud.get_application_status_by_name(db, q.value)
        applications = user_profile_job_crud.get_applications_by_job_id_and_status(db, job_id, application_status.id)

    # check if there were any applications
    if len(applications) == 0:
        if q is None:
            detail = f"No applications found for job {job_id}."
        else:
            detail = f"No applications found for job {job_id} and status {q.value}."
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=detail)

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
    """
    POST route for an applicant user to create a new application for a specific job. The user is
    not allowed to submit multiple applications for the same job.

    Parameters
    ----------
    db: Session
        a dtabase session
    job_id: int
        the job's unique identifier in the database
    applicant: user_model.User
        a sqlalchemy object representing the current authenticated user
    
    Returns
    -------
    user_profile_job_schema.UserProfileJob
        a pydantic model representing the new application in the database
    """

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
    """
    DELETE route to delete for an applicant to delete their own application for a specific job.

    Parameters
    ----------
    db: Session
        a database session
    job_id: int
        a job's unique identifier in the database
    applicant: user_model.User
        a sqlalchemy object representing the current authenticated applicantuser

    Returns
    -------
    str
        A confirmation message that the application was deleted
    """

    # check if the application exists
    application = user_profile_job_crud.get_application_by_user_id_and_job_id(db, applicant.id, job_id)

    if application is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Application for applicant {applicant.id} and job {job_id} not found.")

    user_profile_job_crud.delete_applicant_application(db, applicant.id, job_id)

    # delete the application
    return f"Deleted application for job {job_id} for applicant {applicant.id}."


# PATCH /applications/{job_id}_{applicant_id}/ change status 
@router.patch(
    "/applications/{job_id}_{applicant_id}/",
    response_model=user_profile_job_schema.UserProfileJob,
    status_code=status.HTTP_200_OK,
    tags=["Application"],
    summary="PATCH route for a recruiter to change the status of an application.",
    description="Change the status of an application for a job and provide optional rejection feedback " \
        "for the applicant. The status of an application cannot move backwards. The recruiter must " \
        "own the job to be able to change the status of an application.",
    response_description="The updated application."
)
def change_application_status(db: Session = Depends(dependencies.get_db),
                               job_id: int = Path(),
                               applicant_id: int = Path(),
                               new_status: application_status_model.ApplicationStatusEnum = Body(),
                               rejection_feedback: str | None = Body(default=None),
                               recruiter: user_model.User = Depends(dependencies.get_current_recruiter_user)):
    # Check the application exists
    application = user_profile_job_crud.get_application_by_user_id_and_job_id(db, applicant_id, job_id)
    if application is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Application for job {job_id} and applicant {applicant_id} does not exist."
        )

    # Check the recruiter owns the job
    job = job_crud.get_job_by_id(db, job_id)

    if job.user_profile_id != recruiter.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Recruiter {recruiter.id} is not authorized to update applications for job " \
                "{job_id}."
        )
    
    # Check the current status of the application and the new status of the application to see if it is allowed
    # The new status of an application must be greater or equal to the current status of an application
    # except in the case of REJECTED, which is a final status it can only be equal
    can_change_app_status = False
    new_application_status_id = application_status_crud.get_application_status_by_name(db, new_status.value).id

    if application.application_status.status == application_status_model.ApplicationStatusEnum.rejected.value:
        if new_application_status_id == application.application_status_id:
            can_change_app_status = True
    else:
        if new_application_status_id >= application. application_status_id:
            can_change_app_status = True

    if not can_change_app_status:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot change application status from {application.application_status.status} to "\
                f"{new_status.value}."
        )

    # Update the application status of the application
    return user_profile_job_crud.update_applicant_application_status(db, applicant_id, job_id, new_status, rejection_feedback)

