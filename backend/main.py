from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import crud, models, schemas
from database import SessionLocal, engine

app = FastAPI()

def get_db():
	session = SessionLocal()
	session.execute("SET SEARCH_PATH to cyberhire")
	try:
		yield session
	finally:
		session.close()

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
	existing_user = crud.get_user_by_email(db, user.email)
	if existing_user:
		raise HTTPException(status_code=400, detail="Email already exists.")
	return crud.create_user(db, user)
