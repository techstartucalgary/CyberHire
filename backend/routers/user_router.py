from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..crud import user_crud
from ..models import user_model
from ..schemas import user_schema, token_schema
# from ..database import SessionLocal
from .. import dependencies

router = APIRouter()

# Path Operation Functions

@router.post("/token", response_model=token_schema.Token)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(dependencies.get_db)):
	"""
	Login route to return an access token.
	
	Parameters
	----------
	form: OAuth2PasswordRequestForm
		a pydantic model with username and password attributes
	db: Session
		a database connection

	Returns
	-------
	schemas.Token
		a dict with keys access_token and token_type
	"""
	user = dependencies.authenticate_user(form.username, form.password, db)
	if not user:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Incorrect username or password",
			headers={"WWW-Authenticate": "Bearer"}
		)
	access_token_expires = timedelta(minutes=dependencies.ACCESS_TOKEN_EXPIRE_MINUTES)
	access_token = dependencies.create_access_token(
		data={"sub": user.username},
		expires_delta=access_token_expires
	)
	return {"access_token": access_token, "token_type": "bearer"}


@router.post("/users/", response_model=user_schema.User)
def create_user(user: user_schema.UserCreate, db: Session = Depends(dependencies.get_db)):
	existing_user = user_crud.get_user_by_username(db, user.username)
	if existing_user:
		raise HTTPException(status_code=400, detail="Username already exists.")
	return user_crud.create_user(db, user)

@router.get("/users/me", response_model=user_schema.User)
def get_user_me(user=Depends(dependencies.get_current_user)):
	return user

