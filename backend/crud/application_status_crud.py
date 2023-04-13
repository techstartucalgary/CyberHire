from sqlalchemy.orm import Session

from ..models import application_status_model

def get_application_status_by_name(db: Session, 
                                   status: str) -> application_status_model.ApplicationStatus | None:
    """
    Utility function to get an application status in the datbase by name

    Parameters
    ----------
    db: Session
        a database session
    status: str
        the string value of the application status in the database

    Returns
    -------
    application_status_model.ApplicationStatus
        a sqlalchemy object representing the application status
    """
    
    application_status = db.query(application_status_model.ApplicationStatus)\
        .filter(application_status_model.ApplicationStatus.status == status).first()
    
    return application_status
    