from sqlalchemy.orm import Session
from sqlalchemy import func

from ..models import jobs_model, job_skill_model, user_profile_model, \
                     user_profile_skill_model, user_profile_job_model

def get_job_matching(db: Session, user_id: int) -> list[jobs_model.Job]:
    """
    Utility function to find a list of up to 10 jobs that are the best match
    for the given user. The jobs are ordered descendingly based on the count of skills
    that match between the user and the job. Jobs that an applicant have already
    applied to are filtered out of the list.

    Parameters
    ----------
    db: Session
        a database sesion
    user_id: int
        the user's id in the User table
    
    Returns
    -------
    list[jobs_model.Job]
        a list of sqlalchemy job objects
    """

    # define subquery to match user_profile to user_profile_skills
    q_inner_user = db.query(user_profile_model.UserProfile, user_profile_skill_model.UserProfileSkill)\
        .join(user_profile_skill_model.UserProfileSkill,
              user_profile_skill_model.UserProfileSkill.user_profile_id == user_profile_model.UserProfile.user_id)\
        .filter(user_profile_model.UserProfile.user_id == user_id).subquery(name="C")

    # define subquery to find list of job id's applicant already applied to
    q_inner_applied_jobs = db.query(user_profile_job_model.UserProfileJob.job_id)\
        .filter(user_profile_job_model.UserProfileJob.user_profile_id == user_id)

    # define outerquery to join job to job_skills, then the result joined to the subquery
    q_outer = db.query(jobs_model.Job.id, func.count(jobs_model.Job.id))\
        .join(job_skill_model.JobSkill, job_skill_model.JobSkill.job_id == jobs_model.Job.id)\
        .join(q_inner_user, q_inner_user.c.skill_id == job_skill_model.JobSkill.skill_id)\
        .filter(~jobs_model.Job.id.in_(q_inner_applied_jobs))\
        .group_by(jobs_model.Job.id)\
        .order_by(func.count(jobs_model.Job.id).desc())\
        .limit(10)

    # get a list of job_ids
    job_id_matches = [job_id_and_skill_count[0] for job_id_and_skill_count in q_outer.all()]

    jobs = []
    for job_id in job_id_matches:
        q_jobs = db.query(jobs_model.Job) \
            .filter(jobs_model.Job.id == job_id)
 
        jobs.append(q_jobs.first())

    return jobs
