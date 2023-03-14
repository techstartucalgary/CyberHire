from sqlalchemy.orm import Session
from ..models import skill_model, user_profile_skill_model, \
                     user_profile_model, job_skill_model

def get_skills(db: Session):
    """
    Utility function to return a list of all available skills
    to selct from in the database.

    Parameters
    ----------
    db: Session
        a database connection

    Returns
    -------
    list[models.skill_model.Skill]
        a list of sqlalchemy Skill objects
    """
    return db.query(skill_model.Skill).all()


def get_skills_by_user_id(db: Session, user_id):
    """
    Utility function to get all skills associated with a user id.

    Parameters
    ----------
    db: Session
        a database connection
    user_id: int
        a user id

    Returns
    -------
    list[models.skill_model.Skill]
        a list of sqlalchemy Skill objects
    """

    user_profile = db.query(user_profile_model.UserProfile) \
                        .filter(user_profile_model.UserProfile.user_id == user_id).first()
    if user_profile :
        return user_profile.skills


def get_skill_by_name(db: Session, skill):
    """
    Utility function to get a skill from the database by it's name
    to obtain it's id.

    Parameters
    ----------
    db: Session:
        a database connection
    skill: str
        the name of the skill to retrieve

    Returns
    -------
    models.skill_model.Skill
        a sqlalchemy Skill object
    """

    return db.query(skill_model.Skill).filter(skill_model.Skill.skill == skill).first()


def delete_all_user_profile_skill(db: Session, user_id):
    """
    Utility function to delete all of a user's skills by deleting all
    rows in the user_profile_skill many to many table for the user's id.

    Parameters
    ----------
    db: Session
        a database connection
    user_id: int
        a user id

    Returns
    -------
    int
        the number of rows deleted
    """

    return db.query(user_profile_skill_model.UserProfileSkill) \
        .filter(user_profile_skill_model.UserProfileSkill.user_profile_id == user_id).delete()


def create_user_profile_skill(db: Session, user_id, skill_id):
    """
    Utiltiy function to create a new row in the user_profile_skill many
    to many table.

    Parameters
    ----------
    db: Session
        a database connection
    user_id: int
        a user id
    skill_id: int
        a skill id

    Returns
    -------
    models.skill_model.Skill
        a sqlalchemy Skill object representing the skill that was added to the user profile
    """

    db_user_profile_skill = user_profile_skill_model.UserProfileSkill(
                    user_profile_id=user_id, skill_id=skill_id
                    )
    db.add(db_user_profile_skill)
    db.commit()
    return db.query(skill_model.Skill).filter(skill_model.Skill.id == skill_id).first()

def delete_all_job_skills(db: Session, job_id: int) -> int:
    """
    Utility function to delete all the skills related to a job with id = job_id

    Parameters
    ----------
    db: Session
        a database session
    job_id: int
        the job's id in the database

    Returns
    -------
    int
        the number of rows deleted in the database
    """

    return db.query(job_skill_model.JobSkill).filter(job_skill_model.JobSkill.job_id == job_id).delete()

def create_job_skill(db: Session, job_id: int, skill_id: int) -> skill_model.Skill | None:
    """
    Utility function to create a new skill relationship for a job

    Parameters
    ----------
    db: Session
        a database session
    job_id: int
        the job's id in the database
    skill_id: int
        the skill's id in the database
    """
    db_job_skill = job_skill_model.JobSkill(job_id=job_id, skill_id=skill_id)

    db.add(db_job_skill)
    db.commit()
    return db.query(skill_model.Skill).filter(skill_model.Skill.id == skill_id).first()
