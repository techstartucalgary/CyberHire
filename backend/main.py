from datetime import timedelta
import datetime
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
import crud, schemas
from database import SessionLocal
from passlib.context import CryptContext
from jose import JWTError, jwt

SECRET_KEY = "c22354c13199c37439977b0f2ca2698b84d839bb387b38f59c5edcda787bf6ef"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

password_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI()

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
		encrypted versio of password.
	"""

	return password_ctx.hash(password)

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
	user: models.User
		a sqlsalchemy user object
	"""
	user = crud.get_user_by_username(db, username)
	
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
	models.User | boolean
		False if the user does not exist with the given username in
		the database, or if the password is incorrect.
		models.User if otherwise.
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
		expires = datetime.datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
	else:
		expires = datetime.datetime.utcnow() + expires_delta
	data.update({"exp": expires})
	access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
	return access_token

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
	"""
	Utility function to get the user from the token.
	
	Parameters
	----------
	token: str
		a jwt token
	db: Session
		a database connection

	Returns
	-------
	models.user
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
	except JWTError as e:
		raise credential_exception
	user = get_user(username, db)
	if user is None:
		raise credential_exception
	return user

@app.post("/token", response_model=schemas.Token)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
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

	user = authenticate_user(form.username, form.password, db)
	if not user:
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail="Incorrect username or password"
		)
	access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
	access_token = create_access_token(
		data={"sub": user.username},
		expires_delta=access_token_expires
	)
	return {"access_token": access_token, "token_type": "bearer"}


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
	existing_user = crud.get_user_by_username(db, user.username)
	if existing_user:
		raise HTTPException(status_code=400, detail="Username already exists.")
	return crud.create_user(db, user)

@app.get("/users/me", response_model=schemas.User)
def get_user_me(user=Depends(get_current_user)):
	return user