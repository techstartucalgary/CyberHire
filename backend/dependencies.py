from .database import SessionLocal
from .models import user_model
from .crud import user_crud, user_profile_crud
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, status, HTTPException
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import timedelta, datetime

password_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
ACCESS_TOKEN_EXPIRE_MINUTES = 30
SECRET_KEY = "c22354c13199c37439977b0f2ca2698b84d839bb387b38f59c5edcda787bf6ef"
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Utility Functions

def verify_password(plain_password: str, hashed_password: str):
	"""
	Utility function to verify a password.

	Parameters
	----------
	plain_password: str
		a user's unencrypted password to verify.
	hashed_password: str
		a user's encrpyted password.

	Returns
	-------
	bool
		True if the encrypted plain_password matches hashed_password.
	"""

	return password_ctx.verify(plain_password, hashed_password)

def get_password_hash(password):
	"""
	Utility function to hash a password.
	
	Parameters
	----------
	password: str
		a unencrypted password.

	Returns
	-------
	str
		encrypted version of password.
	"""

	return password_ctx.hash(password)

def get_user(username: str, db: Session):
	"""
	Utility function to get a user from the database.
	
	Parameters
	----------
	username: str
		a user's username
	db: Session
		a database connection

	Returns
	-------
	user: models.user_model.User
		a sqlsalchemy user object
	"""
	
	user = user_crud.get_user_by_username(db, username)
	
	return user

def authenticate_user(username: str, password: str, db: Session):
	"""
	Utility function to authenticate a user.
	
	Parameters
	----------
	username: str
		a user's username
	password: str
		a user's unencrypted password.
	db: Session
		a database connection

	Returns
	-------
	models.user_model.User | boolean
		False if the user does not exist with the given username in
		the database, or if the password is incorrect.
		models.user_model.User if otherwise.
	"""

	user = get_user(username, db)
	if user is None:
		return False
	if not verify_password(password, user.password):
		return False
	return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
	"""
	Utility function to create a JWT token for login.
	
	Parameters
	----------
	data: dict
		a dictionary with the sub key that contains the user's username
	expires_delta: timedelta
		expiry time of the token
	
	Returns
	-------
	access_token: str
		a jwt token
	"""

	if expires_delta is None:
		expires = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
	else:
		expires = datetime.utcnow() + expires_delta
	data.update({"exp": expires})
	access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
	return access_token

def user_profile_exists(db: Session, id):
	"""
	Utility function to check if a user has an associated profile
	in the user_profile table in the database.

	Parameters
	----------
	db: Session
		a database session
	id: a user id

	Raises
	------
	HTTPException
		if the there is no associated profile with the user id given
	"""
	database_user_profile = user_profile_crud.get_user_profile_by_id(db, id)

	if database_user_profile is None:
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail="User does not have a database profile. Please create one first."
			)

# Dependencies

def get_db():
	"""
	Dependency function to get a database instance.
	
	Parameters
	----------
	None

	Returns
	-------
	Session
		a database session
	"""

	session = SessionLocal()
	session.execute("SET SEARCH_PATH to cyberhire")
	try:
		yield session
	finally:
		session.close()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
	"""
	Dependency function to get the user from the token.
	
	Parameters
	----------
	token: str
		a jwt token
	db: Session
		a database connection

	Returns
	-------
	models.user_model.user
		a sqlalchemy user object representing the current user
	"""

	credential_exception = HTTPException(
		status_code=status.HTTP_401_UNAUTHORIZED,
		detail="Could not validate credentials.",
		headers={"WWW-Authenticate": "Bearer"}
	)
	try:
		payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
		username = payload.get("sub")
		if username is None:
			raise credential_exception
	except JWTError:
		raise credential_exception
	user = get_user(username, db)
	if user is None:
		raise credential_exception
	return user

def get_current_recruiter_user(current_user: user_model.User = Depends(get_current_user)):
	"""
	Dependency function to get and authorize a recruiter user.

	Parameters
	----------
	current_user : models.User
		a sqlalchemy user object representing the current user
	
	Returns
	-------
	models.user_model.User
		a sqlalchemy user object representing the current recruiter user
	"""

	if not current_user.is_recruiter:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not recruiter.")
	return current_user

def get_current_applicant_user(current_user: user_model.User = Depends(get_current_user)):
	"""
	Dependency function to get and authorize an applicant user.

	Parameters
	----------
	current_user : models.User
		a sqlalchemy user object representing the current user
	
	Returns
	-------
	models.user_model.User
		a sqlalchemy user object representing the current applicant user
	"""

	if current_user.is_recruiter:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not applicant.")
	return current_user