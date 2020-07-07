from sqlalchemy import Boolean, Column, ForeignKey, Integer, Unicode
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_imageattach.entity import Image, image_attachment

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Unicode)
    username = Column(Unicode, unique=True, index=True)
    email = Column(Unicode)
    hashed_password = Column(Unicode)
    is_active = Column(Boolean, default=True)

    questions = relationship("Question", back_populates="creator", uselist=True)


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    header = Column(Unicode, index=True)
    details = Column(Unicode, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    pictures = image_attachment("QuestionPicture", uselist=True)
    creator = relationship("User", back_populates="questions")


class QuestionPicture(Base, Image):
    """Model for pictures associated with the question."""

    __tablename__ = "question_pictures"

    id = Column(Integer, primary_key=True)
    # Not sure if the question ID should also be a unique identifier
    question_id = Column(Integer, ForeignKey("question.id"), primary_key=True)
    question = relationship("Question")

