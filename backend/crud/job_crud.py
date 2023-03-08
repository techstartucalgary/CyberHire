from sqlalchemy.orm import Session
from ..models import jobs_model
from ..schemas import job_schema

def get_all_jobs(db: Session):

    return db.query(jobs_model.Job).all()

def get_job_by_id(db: Session, job_id: int):

    return db.query(jobs_model.Job).filter(jobs_model.Job.id == job_id).first()

def get_jobs_by_user_profile_id(db: Session, user_profile_id: int):

    return db.query(jobs_model.Job).filter(jobs_model.Job.user_profile_id == user_profile_id).all()

def create_job(db: Session, user_profile_id: int, new_job: job_schema.JobCreate):

    # Convert pydantic schema to a sql alchemy model
    new_job_model = jobs_model.Job(user_profile_id=user_profile_id, **new_job.dict())

    db.add(new_job_model)
    db.commit()
    db.refresh(new_job_model)

    return new_job_model