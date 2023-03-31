from datetime import datetime

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

def get_applications_by_job_id_and_status(db: Session,
                                          job_id: int,
                                          q: application_status_model.ApplicationStatusEnum) \
                                          -> list[user_profile_job_model.UserProfileJob]:
    
    return db.query(user_profile_job_model.UserProfileJob) \
            .filter(user_profile_job_model.UserProfileJob.job_id == job_id and
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

def create_applicant_application(db: Session, user_id: int, job_id: int) \
                                -> user_profile_job_model.UserProfileJob:
    
    new_application = user_profile_job_model.UserProfileJob(
        user_profile_id=user_id,
        job_id=job_id,
        application_status_id=application_status_model.ApplicationStatusEnum.submitted.value,
        application_submitted_date=datetime.today(),
        application_reviewed_date=None,
        application_offer_sent_date=None,
        application_rejected_date=None
    )

    db.add(new_application)
    db.commit()
    db.refresh(new_application)
    return new_application

def delete_applicant_application(db: Session, user_id: int, job_id: int) \
                                 -> user_profile_job_model.UserProfileJob:
    

    
def update_applicant_application_status(db: Session, user_id: int, job_id: int, 
                                        new_status: application_status_model.ApplicationStatusEnum) \
                                        -> user_profile_job_model.UserProfileJob:

    application = get_application_by_user_id_and_job_id(db, user_id, job_id)
    application.application_status_id = new_status.value
    #application.application_reviewed_date = datetime.today()
    db.save(application)
    db.commit()
    db.refresh(application)
    return application