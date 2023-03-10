from sqlalchemy.orm import Session
from ..models import jobs_model
from ..schemas import job_schema

def get_all_jobs(db: Session) -> list[jobs_model.Job]:

    return db.query(jobs_model.Job).all()

def get_job_by_id(db: Session, job_id: int) -> jobs_model.Job | None:

    return db.query(jobs_model.Job).filter(jobs_model.Job.id == job_id).first()

def get_jobs_by_user_profile_id(db: Session, user_profile_id: int) -> list[jobs_model.Job]:

    return db.query(jobs_model.Job).filter(jobs_model.Job.user_profile_id == user_profile_id).all()

def create_job(db: Session, user_profile_id: int, new_job: job_schema.JobCreate) -> jobs_model.Job:

    # Convert pydantic schema to a sql alchemy model
    new_job_model = jobs_model.Job(user_profile_id=user_profile_id, **new_job.dict())

    db.add(new_job_model)
    db.commit()
    db.refresh(new_job_model)

    return new_job_model

def update_job(db: Session, new_job: job_schema.JobInDb) -> jobs_model.Job | None:

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