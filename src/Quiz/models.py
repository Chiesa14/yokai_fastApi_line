from sqlalchemy import Column, JSON
from sqlmodel import Field, SQLModel, Relationship
from typing import List, Optional
from enum import Enum


class QuizType(str, Enum):
    MANGA_STORIES = "manga stories"
    PERSONALITY_ASSESSMENT = "personality-assessment"
    COMPLIMENT = "compliment"


class QuestionData(SQLModel):
    question: str
    options: Optional[List[str]] = None 
    correct_answer: Optional[List[int]] = None  
    personality_trait: Optional[str] = None
    line_friend: Optional[str] = None


class QuizBase(SQLModel):
    quiz_type: QuizType
    title: str
    description: Optional[str] = None
    questions: Optional[List[QuestionData]] = Field(default=None, sa_column=Column(JSON))


class QuizCreate(QuizBase):
    pass


class Quiz(QuizBase, table=True):
    __tablename__ = "quiz_table"
    id: Optional[int] = Field(default=None, primary_key=True)


class AnswerBase(SQLModel):
    question_index: int  
    selected_answer: Optional[int] = None 
    selected_answers: Optional[List[int]] = Field(default=None, sa_column=Column(JSON))
    answer_text: Optional[str] = None


class Answer(AnswerBase, table=True):
    __tablename__ = "answer_table"
    id: Optional[int] = Field(default=None, primary_key=True)


class QuizSubmission(SQLModel):
    quiz_id: int
    user_id: Optional[int] = None
    answers: List[AnswerBase]
