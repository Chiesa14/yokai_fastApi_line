from fastapi import FastAPI, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from src.database import get_db  # Assuming a database session is available
from .service import create_referral_code, get_referral_code_by_user_id

router = APIRouter()

@router.post("/referral-code/")
def generate_referral_code(user_id: int, db: Session = Depends(get_db)):
        return create_referral_code(db=db, user_id=user_id)

@router.get("/referral-code/{user_id}")
def retrieve_referral_code(user_id: int, db: Session = Depends(get_db)):
        return  get_referral_code_by_user_id(db, user_id)
