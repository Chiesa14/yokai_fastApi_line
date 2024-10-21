from typing import List
from fastapi import APIRouter, Depends
from sqlmodel import Session
from .models import Quiz, QuizCreate, Answer
from src.database import get_db
from .service import create_quiz, get_all_quizzes, get_quiz_by_id, submit_quiz_answers

router = APIRouter()


# Endpoint to create a new quiz with embedded questions
@router.post("/new", response_model=Quiz)
async def create_new_quiz(quiz_data: QuizCreate, db: Session = Depends(get_db)):
    return create_quiz(db, quiz_data)


# Route to fetch all quizzes
@router.get("/")
async def fetch_quizzes(db: Session = Depends(get_db)):
    quizzes = get_all_quizzes(db)
    return {"quizzes": quizzes}


# Route to get a quiz by ID
@router.get("/{quiz_id}")
async def fetch_quiz_by_id(quiz_id: int, db: Session = Depends(get_db)):
    quiz = get_quiz_by_id(db, quiz_id)
    return quiz


# Route to submit answers for a quiz
@router.post("/quizzes/{quiz_id}/submit")
async def submit_answers(quiz_id: int, user_id: int, answers: List[Answer], db: Session = Depends(get_db)):
    return await submit_quiz_answers(db, quiz_id, user_id, answers)
