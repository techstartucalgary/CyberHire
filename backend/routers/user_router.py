from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import EmailStr
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..crud import user_crud
from ..models import user_model
from ..schemas import user_schema, token_schema
from .. import dependencies

router = APIRouter()

# Path Operation Functions

@router.post(
	"/token", 
	response_model=token_schema.Token, 
	status_code=status.HTTP_200_OK,
	tags=["User"],
	summary="Login route to return an access token.",
	description="Return an access token if authenticated, otherwise return a 401 status code.",
	response_description="The access token."
	)
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
	schemas.token_schema.Token
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


@router.post(
	"/users/", 
	response_model=user_schema.User,
	summary="Create a new user.",
	description="Create a new user with all information, including username, email, is_recruiter, and password.",
	status_code=status.HTTP_201_CREATED,
	tags=["User"],
	response_description="The created user."
	)
def create_user(user: user_schema.UserCreate, db: Session = Depends(dependencies.get_db)):
	"""
	Create route to create a new user.

	Parameters
	----------
	user: user.user_schema.UserCreate
		A pydantic model for creating a new user.
	db: Session
		a database connection

	Returns
	-------
	schema.user_schema.User
		A pydantic model user object representing the user created in the database.
	"""

	existing_user_username = user_crud.get_user_by_username(db, user.username)
	existing_user_email = user_crud.get_user_by_email(db, user.email)
	if existing_user_username or existing_user_email:
		raise HTTPException(status_code=400, detail="Username or email already exists.")
	return user_crud.create_user(db, user)

@router.delete(
	"/users/me",
	response_model=user_schema.User,
	summary="Delete a user from the database.",
	description="Delete a applicant or a recruiter from the database if their account is no longer required.",
	status_code=status.HTTP_200_OK,
	tags=["User"],
	response_description="The deleted user."
)
def delete_user_me(user: user_model.User = Depends(dependencies.get_current_user), db: Session = Depends(dependencies.get_db)):
	"""
	A delete route for deleting a user from the database.

	Parameters
	----------
	user: models.user_model.User
		a sqlalchemy user object representing the current user
	db: Session
		a database connection

	Returns
	-------
	schemas.user_schema.User
		a pydantic user object representing the deleted user
	"""
	existing_user = user_crud.get_user_by_username(db, str(user.username))
	if not existing_user:
		raise HTTPException(
			status_code=400,
			detail="Username does not exist."
		)
	return user_crud.delete_user_by_username(db, str(user.username))

@router.patch(
	"/users/me",
	response_model=user_schema.User,
	summary="Update a user's account information",
	description="Update a applicant or a recruiter's account information, including username, email, is_recruiter, and password.",
	status_code=status.HTTP_200_OK,
	tags=["User"],
	response_description="The user's updated account information, including username, email, is_recruiter, and id."
)
def patch_user_me(*, 
	current_user_data: user_model.User = Depends(dependencies.get_current_user), 
	new_user_data: user_schema.UserPatch,
	db: Session = Depends(dependencies.get_db)
):
	"""
	A patch route for the current user to update their account information.
	Only the information that is provided by the user is updated.
	For example, if the user only passes in a new password, then only the password is updated.

	Parameters
	----------
	current_user_data: user_model.User
		a sqlalchemy User object representing the current user
	new_user_data: user_schema.UserPatch
		a pydantic model representing the current user's new account information
	db: Session
		a connection to the database

	Returns
	-------
	user_schema.User
		The current user's new account information
	"""
	if new_user_data.username:
		existing_user = user_crud.get_user_by_username(db, new_user_data.username)
		if existing_user and current_user_data.id != existing_user.id:
			raise HTTPException(
				status_code=status.HTTP_400_BAD_REQUEST,
				detail="Username is already taken by another user."
			)
	if new_user_data.email:
		existing_user = user_crud.get_user_by_email(db, new_user_data.email)
		if existing_user and current_user_data.id != existing_user.id:
			raise HTTPException(
				status_code=status.HTTP_400_BAD_REQUEST,
				detail="Email is already taken by another user."
			)
		
	current_user_model = user_schema.UserInDb(
		id=int(str(current_user_data.id)),
		username=str(current_user_data.username),
		email=EmailStr(current_user_data.email),
		is_recruiter=bool(current_user_data.is_recruiter),
		hashed_password=str(current_user_data.password)
	)
	update_data = new_user_data.dict(exclude_unset=True)
	if new_user_data.password:
		update_data["hashed_password"] = dependencies.get_password_hash(new_user_data.password)
	updated_user = current_user_model.copy(update=update_data)
	
	return user_crud.update_user(db, updated_user)

@router.get(
	"/users/me", 
	response_model=user_schema.User,
	summary="Return current user information.",
	description="Return current user information, including username, email, is_recruiter, and id.",
	status_code=status.HTTP_200_OK,
	tags=["User"],
	response_description="The current user."
	)
def get_user_me(user: user_model.User = Depends(dependencies.get_current_user)):
	"""
	A get route for the current user's data

	Parameters
	----------
	user: models.user_model.User
		a sqlalchemy user object representing the current user
	
	Returns
	-------
	schames.user_schema.User
		a pydantic user object representing the current user
	"""
	return user

