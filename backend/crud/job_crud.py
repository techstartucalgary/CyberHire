from sqlalchemy.orm import Session
from ..models import jobs_model
from ..schemas import job_schema

def get_all_jobs(db: Session) -> list[jobs_model.Job]:
    """
    Utility function to return all jobs in the database

    Parameters
    ----------
    db: Session
        a database session

    Returns
    -------
    list[jobs_model.Job]
        list of sqlalchemy Job objects
    """

    return db.query(jobs_model.Job).all()

def get_job_by_id(db: Session, job_id: int) -> jobs_model.Job | None:
    """
    Utility function to return a job by job id

    Parameters
    ----------
    db: Session
        a database sesion
    job_id:
        the job's id in the database

    Returns
    -------
    jobs_model.Job | None
        a sqlalchemy Job object, or None if no job with the id is found
    """

    return db.query(jobs_model.Job).filter(jobs_model.Job.id == job_id).first()

def get_jobs_by_user_profile_id(db: Session, user_profile_id: int) -> list[jobs_model.Job]:
    """
    Utility function to get all jobs posted by a recruiter

    Parameters
    ----------
    db: Session
        a database session
    user_profile_id: int
        the recruiters id

    Returns
    -------
    list[jobs_model.Job]
        a list of sqlalchemy Job objects that were posted by the recruiter
    """

    return db.query(jobs_model.Job).filter(jobs_model.Job.user_profile_id == user_profile_id).all()

def create_job(db: Session, user_profile_id: int, new_job: job_schema.JobCreate) -> jobs_model.Job:
    """
    Utility function to create a new job for the recruiter with id = user_profile_id

    Parameters
    ----------
    db: Session
        a database session
    user_profile_id: int
        the recruiters id
    new_job: job_schema.JobCreate
        a pydantic model for creating a new job

    Returns
    jobs_model.Job
        a sqlalchemy Job object representing the newly created Job
    """

    # Convert pydantic schema to a sql alchemy model
    new_job_model = jobs_model.Job(user_profile_id=user_profile_id, **new_job.dict())

    db.add(new_job_model)
    db.commit()
    db.refresh(new_job_model)

    return new_job_model

def update_job(db: Session, new_job: job_schema.JobInDb) -> jobs_model.Job | None:
    """
    Utility function to update a job in the database

    Parameters
    ----------
    db: Session
        a database session
    new_job: job_schema.JobInDb
        a pydantic model with the updated job information

    Returns
    -------
    jobs_model.Job | None
        a sqlalchemy Job object with the updated information, or None if no job is found
    """

    current_job = db.query(jobs_model.Job).filter(jobs_model.Job.id == new_job.id).first()

    if current_job is not None:
        current_job.title = new_job.title
        current_job.description = new_job.description
        current_job.location = new_job.location
        current_job.min_salary = new_job.min_salary
        current_job.max_salary = new_job.max_salary
    db.commit()
    db.refresh(current_job)
    return current_job

def delete_job(db: Session, job_id: int) -> jobs_model.Job | None:
    """
    Utility function to delete a job with job id = job_id from the database

    Parameters
    ----------
    db: Session
        a database session
    job_id: int
        the job's id in the database

    Returns
    -------
    jobs_model.Job | None
        a sqlalchemy object representing the job that was deleted, or None if no job was found
    """

    job_in_db = get_job_by_id(db, job_id)
    job_in_db_copy = None

    if job_in_db is not None:
        job_in_db_copy = jobs_model.Job(
            id=job_in_db.id,
            user_profile_id=job_in_db.user_profile_id,
            description=job_in_db.description,
            title=job_in_db.title,
            location=job_in_db.location,
            min_salary=job_in_db.min_salary,
            max_salary=job_in_db.max_salary
        )

        db.delete(job_in_db)
        db.commit()

    return job_in_db_copy
