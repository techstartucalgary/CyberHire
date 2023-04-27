from datetime import datetime

from sqlalchemy.orm import Session

from ..models import application_status_model, user_profile_job_model
from ..crud import application_status_crud

def get_applications_by_user_id(db: Session,
                                user_id: int) -> list[user_profile_job_model.UserProfileJob]:
    """
    Utility function to return all applications in the database for a given applicant user.

    Parameters
    ----------
    db: Session
        a database session
    user_id: int
        the applicant user's id in the User table

    Returns
    -------
    list[user_profile_job_model.UserProfileJob]
        a list of all a user's applications
    """

    return db.query(user_profile_job_model.UserProfileJob) \
        .filter(user_profile_job_model.UserProfileJob.user_profile_id == user_id).all()

def get_applications_by_user_id_and_status(db: Session,
                                           user_id: int,
                                           q: int) \
                                            -> list[user_profile_job_model.UserProfileJob]:
    """
    Utility function to return all applications in the database for a given application user
    and application status type

    Parameters
    ----------
    db: Session
        a database session
    user_id: int
        a user's unique identifier in the database
    q: application_status_model.ApplicationStatusEnum
        enumeration of application status

    Returns
    -------
    list[user_profile_job_model.UserProfileJob]
        a list of all a user's applications for a given application status type
    """

    return db.query(user_profile_job_model.UserProfileJob) \
        .filter(user_profile_job_model.UserProfileJob.user_profile_id == user_id) \
        .filter(user_profile_job_model.UserProfileJob.application_status_id == q).all()

def get_applications_by_job_id_and_status(db: Session,
                                          job_id: int,
                                          q: int) \
                                          -> list[user_profile_job_model.UserProfileJob]:
    """
    Utility function to get all applications for a given job with a specific application
    status type

    Parameters
    ----------
    db: Session
        a database session
    job_id: int
        a job's unique identifier in the database
    q: application_status_model.ApplicationStatusEnum
        enumeration of application status

    Returns
    -------
    list[user_profile_job_model.UserProfileJob]
        a list of all applications for a given job with a given application status type
    """

    return db.query(user_profile_job_model.UserProfileJob) \
            .filter(user_profile_job_model.UserProfileJob.job_id == job_id) \
            .filter(user_profile_job_model.UserProfileJob.application_status_id == q).all()

def get_application_by_user_id_and_job_id(db: Session,
                                          user_id: int,
                                          job_id: int) -> user_profile_job_model.UserProfileJob | None:
    
    """
    Utility function to get a user's application for a specific job

    Parameters
    ----------
    db: Session
        a database session
    user_id: int
        a user's unique identifier in the database
    job_id: int
        a job's unique identifier in the database

    Returns
    -------
    user_profile_job_model.UserProfileJob | None
        the user's application for the specified job, or None if the application
        does not exist
    """

    return db.query(user_profile_job_model.UserProfileJob) \
        .filter(user_profile_job_model.UserProfileJob.user_profile_id == user_id) \
        .filter(user_profile_job_model.UserProfileJob.job_id == job_id).first()

def get_applications_by_job_id(db: Session, job_id: int) -> list[user_profile_job_model.UserProfileJob]:
    """
    Utility function to get all applications for a speicific job

    Parameters
    ----------
    db: Session 
        a database session
    job_id: int
        a job's unique identifier in the database

    Returns
    -------
    list[user_profile_job_model.UserProfileJob]
        a list of all the applications for a given job
    """

    return db.query(user_profile_job_model.UserProfileJob) \
        .filter(user_profile_job_model.UserProfileJob.job_id == job_id).all()

def create_applicant_application(db: Session, user_id: int, job_id: int) \
                                -> user_profile_job_model.UserProfileJob:
    """
    Utility function to create a new application in the database for a given job and
    applicant user

    Parameters
    ----------
    db: Session
        a database session
    user_id: int
        a user's unique identifier in the database
    job_id: int
        a job's unique identifier in the database

    Returns
    -------
    user_profile_job_model.UserProfileJob
        a sqlalchemy UserProfileJob object representing the new application
    """
    application_status_id = application_status_crud\
        .get_application_status_by_name(db, application_status_model.ApplicationStatusEnum.submitted).id

    new_application = user_profile_job_model.UserProfileJob(
        user_profile_id=user_id,
        job_id=job_id,
        application_status_id=application_status_id,
        application_submitted_date=datetime.today(),
        application_reviewed_date=None,
        application_offer_sent_date=None,
        application_rejected_date=None,
        rejection_feedback=None
    )

    db.add(new_application)
    db.commit()
    db.refresh(new_application)
    return new_application

def delete_applicant_application(db: Session, user_id: int, job_id: int) \
                                 -> user_profile_job_model.UserProfileJob | None:
    """
    Utility function to delete a user's application for a specific job from the database

    Parameters
    ----------
    db: Session
        a database session
    user_id: int
        a user's unique identifier in the database
    job_id: int
        a job's unique identifier in the database

    Returns
    -------
    user_profile_job_model.UserProfileJob | None
        a sqlalchemy object representing the application that was deleted from the database
    """

    application = db.query(user_profile_job_model.UserProfileJob) \
        .filter(user_profile_job_model.UserProfileJob.user_profile_id == user_id) \
        .filter(user_profile_job_model.UserProfileJob.job_id == job_id) \
        .first()

    db.delete(application)
    db.commit()
    return application

def update_applicant_application_status(db: Session,
                                        user_id: int, 
                                        job_id: int,
                                        new_status: application_status_model.ApplicationStatusEnum,
                                        rejection_feedback: str | None) \
                                        -> user_profile_job_model.UserProfileJob:
    # Get the application
    current_application = get_application_by_user_id_and_job_id(db, user_id, job_id)

    # Get the id for the new application status
    new_application_status_id = application_status_crud.get_application_status_by_name(db, new_status.value).id 

    # Update the current applications id
    current_application.application_status_id = new_application_status_id

    # Update the other attributes of the current application depending on the new status
    if new_status.value == application_status_model.ApplicationStatusEnum.submitted.value:
        current_application.application_submitted_date = datetime.today()
    elif new_status.value == application_status_model.ApplicationStatusEnum.in_review.value:
        current_application.application_reviewed_date = datetime.today()
    elif new_status.value == application_status_model.ApplicationStatusEnum.screening.value:
        current_application.application_further_screening_date = datetime.today()
    elif new_status.value == application_status_model.ApplicationStatusEnum.rejected.value:
        current_application.application_rejected_date = datetime.today()
        current_application.rejection_feedback = rejection_feedback
    elif new_status.value == application_status_model.ApplicationStatusEnum.offer_sent.value:
        current_application.application_offer_sent_date = datetime.today()

    db.commit()
    db.refresh(current_application)
    return current_application
