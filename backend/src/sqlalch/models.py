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
    # questions = relationship("Question", back_populates="creator")


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
    # Not sure if the question ID should also be a unique identifier
    # question_id = Column(Integer, ForeignKey("questions.id"), primary_key=True)
    question_id = Column(Integer, ForeignKey("questions.id"))
    question = relationship("Question", back_populates="pictures")

