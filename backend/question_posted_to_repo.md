I am trying to use `imageattach`, and I do not really understand how it should work, how dis/similar it is to just a normal `relationship`.

Below is a snippet of code, which is mimicking something like a StackOverflow question board, where *users* could post *questions* and the questions could have *images* attached to them.  I am following a style quite similar to [FastAPI's SQLAlchemy tutorial](https://fastapi.tiangolo.com/tutorial/sql-databases/).

I am able to get users, create users, and get questions.  But when I try to create a question (POST a question), I get the following `pydantic` validation error:

```python
pydantic.error_wrappers.ValidationError: 1 validation error for Question
response -> pictures
  value is not a valid list (type=type_error.list)
```

I am fairly sure this is an issue with pydantic having trouble understanding the relationship that *sqlalchemy-imageattach* creates, which is why I am posting here.

---

`schemas.py` (Pydantic models)

```python
from typing import List, Optional
from pydantic import BaseModel

class QuestionPictureBase(BaseModel):
    pass

class QuestionPicture(QuestionPictureBase):
    id: int
    question_id: int
    class Config:
        orm_mode = True

class QuestionBase(BaseModel):
    header: str
    details: str

class QuestionCreate(QuestionBase):
    pass

class Question(QuestionBase):
    id: int
    creator_id: int
    pictures: List[QuestionPicture] = []

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    email: Optional[str] = None
    name: str  # This is the nickname they want to go by
    username: str  # This is the unique user name

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    questions: List[Question] = []

    class Config:
        orm_mode = True
```

Then the SQL ORM models:

`models.py` 

```python
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_imageattach.entity import Image, image_attachment

from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    username = Column(String, unique=True, index=True)
    email = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    questions = relationship("Question", back_populates="creator", uselist=True)

class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True, index=True)
    header = Column(String, index=True)
    details = Column(String, index=True)
    creator_id = Column(Integer, ForeignKey("users.id"))
    pictures = image_attachment("QuestionPicture", uselist=True)
    creator = relationship("User", back_populates="questions")

class QuestionPicture(Base, Image):
    """Model for pictures associated with the question."""
    __tablename__ = "question_pictures"
    id = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey("questions.id"))
    question = relationship("Question", back_populates="pictures")
```

Then the CRUD module (edited down to just the function of interest):

`crud.py`

```python
from sqlalchemy.orm import Session
from . import models, schemas

def create_user_question(db: Session, question: schemas.QuestionCreate, username: str):
    user = get_user_by_username(db=db, username=username)
    db_item = models.Question(**question.dict(), creator_id=user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
```

And finally, the `main.py` module, again edited just to focus upon question creation.

```python
from typing import List
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal, engine

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/{username}/questions/", response_model=schemas.Question)
def create_question_for_user(
    username: str, question: schemas.QuestionCreate, db: Session = Depends(get_db)
):
    return crud.create_user_question(db=db, question=question, username=username)
```

