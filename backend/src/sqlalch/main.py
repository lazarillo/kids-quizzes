from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

# The line below is commented out: Create DBs via Alembic instead of here
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(
            status_code=400, detail=f"Nickname '{user.username}' already registered"
        )
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{username}", response_model=schemas.User)
def read_user(username: str, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=username)
    if db_user is None:
        raise HTTPException(
            status_code=404, detail=f"User nickname '{username}' not found"
        )
    return db_user


@app.post("/users/{username}/questions/", response_model=schemas.Question)
def create_question_for_user(
    username: str, question: schemas.QuestionCreate, db: Session = Depends(get_db)
):
    print(f"You are sending {username} and {question}")
    return crud.create_user_question(db=db, question=question, username=username)


@app.get("/questions/", response_model=List[schemas.Question])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    questions = crud.get_questions(db, skip=skip, limit=limit)
    return questions
