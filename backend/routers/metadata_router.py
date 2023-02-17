from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from ..schemas import skill_schema
from .. import dependencies
from ..crud import skill_crud

# Router for metadata information
router = APIRouter()

@router.get(
    "/skills",
    response_model = list[skill_schema.Skill],
    status_code=status.HTTP_200_OK,
    tags=["Skill"],
    summary="Get a list of all the available skills to select from.",
    description="Get a list of all available skills in the database with their id's and name.",
    response_description="A list of all the available skills in the database."
)
def get_skills(db: Session = Depends(dependencies.get_db)):
    """
    A GET route to get a list of available skills to select from.

    Parameters
    ----------
    db: Session
        a database connection.

    Returns
    -------
    list[skill_schema.Skill]
        a list of pydantic model skill objects.
    """

    return skill_crud.get_skills(db)
