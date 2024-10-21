from typing import List
from sqlmodel import Session, select
from .models import Quiz, QuizCreate, AnswerBase, QuizSubmission, Answer
from fastapi import HTTPException
from sqlalchemy.orm import selectinload


# Service to create a new quiz with embedded questions
def create_quiz(db: Session, quiz_data: QuizCreate) -> Quiz:
    db_quiz = Quiz(**quiz_data.dict())
    db.add(db_quiz)
    db.commit()
    db.refresh(db_quiz)
    return db_quiz


# Service to get all quizzes in the database
def get_all_quizzes(db: Session):
    statement = select(Quiz)
    result = db.exec(statement).all()
    if not result:
        raise HTTPException(status_code=404, detail="No quizzes found")
    return result


# Service to get a specific quiz by ID
def get_quiz_by_id(db: Session, quiz_id: int):
    statement = select(Quiz).where(Quiz.id == quiz_id)
    result = db.exec(statement).first()
    if not result:
        raise HTTPException(status_code=404, detail=f"Quiz with ID {quiz_id} not found")
    return result


# Service to submit answers to a quiz
async def submit_quiz_answers(db: Session, quiz_id: int, user_id: int, user_answers: List[AnswerBase]):
    try:
        quiz = get_quiz_by_id(db, quiz_id)
        if not quiz:
            raise HTTPException(status_code=404, detail="Quiz not found")

        for answer in user_answers:
            if answer.question_index >= len(quiz.questions):
                raise HTTPException(status_code=400, detail=f"Invalid question index {answer.question_index}")

            question = quiz.questions[answer.question_index]

            # Validate answer based on the question type
            if question["type"] == "multiple-choice":
                if answer.selected_answer not in question["correct_answer"]:
                    raise HTTPException(status_code=400, detail=f"Incorrect answer for question {answer.question_index}")
            elif question["type"] == "text":
                pass  # We assume that text answers don't need strict validation
            elif question["type"] == "personality-assessment":
                pass  # Handle personality assessments
            elif question["type"] == "compliment":
                pass  # Store compliments, no validation needed

            db_answer = Answer(**answer.dict())
            db.add(db_answer)

        db.commit()
        return {"message": "Answers were successfully submitted"}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
