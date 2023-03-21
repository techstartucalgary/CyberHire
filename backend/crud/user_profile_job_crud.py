from sqlalchemy.orm import Session

from ..models import application_status_model, user_profile_job_model

def get_applications_by_user_id(db: Session, user_id: int) -> list[user_profile_job_model.UserProfileJob]:

    return db.query(user_profile_job_model.UserProfileJob) \
        .filter(user_profile_job_model.UserProfileJob.user_profile_id == user_id).all()

def get_applications_by_user_id_and_status(db: Session,
                                          user_id: int, 
                                          q: application_status_model.ApplicationStatusEnum) \
                                            -> list[user_profile_job_model.UserProfileJob]:
    
    return db.query(user_profile_job_model.UserProfileJob) \
        .filter(user_profile_job_model.UserProfileJob.user_profile_id == user_id and
                user_profile_job_model.UserProfileJob.application_status_id == q.value).all()

def get_application_by_user_id_and_job_id(db: Session,
                                          user_id: int,
                                          job_id: int) -> user_profile_job_model.UserProfileJob | None:
    
    return db.query(user_profile_job_model.UserProfileJob) \
        .filter(user_profile_job_model.UserProfileJob.user_profile_id == user_id and
                user_profile_job_model.UserProfileJob.job_id == job_id).first()

def get_applications_by_job_id(db: Session, job_id: int) -> list[user_profile_job_model.UserProfileJob]:

    return db.query(user_profile_job_model.UserProfileJob) \
        .filter(user_profile_job_model.UserProfileJob.job_id == job_id).all()
