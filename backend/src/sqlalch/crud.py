from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"  # Come back and fix this
    db_user = models.User(
        email=user.email,
        hashed_password=fake_hashed_password,
        name=user.name,
        username=user.username,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_questions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Question).offset(skip).limit(limit).all()


def create_user_question(db: Session, question: schemas.QuestionCreate, username: str):
    user = get_user_by_username(db=db, username=username)
    db_item = models.Question(**question.dict(), creator_id=user.id)
    print(f"I received {db_item}")
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
