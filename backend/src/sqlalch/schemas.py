from typing import List, Optional

from pydantic import BaseModel


class QuestionPictureBase(BaseModel):
    question_id: int


class QuestionPicture(QuestionPictureBase):
    id: int

    class Config:
        orm_mode = True


class QuestionBase(BaseModel):
    header: str
    details: str


class QuestionCreate(QuestionBase):
    pass


class Question(QuestionBase):
    id: int
    owner_id: int
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
