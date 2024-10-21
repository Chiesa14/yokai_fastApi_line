from fastapi import FastAPI, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from src.ReferalInvitation.service import handle_user_signup_with_referral, get_invitation_by_referral_code
from src.database import get_db

router = APIRouter()

@router.post("/signup-with-referral")
def signup_with_referral(referred_user_id: int, referral_code: str, db: Session = Depends(get_db)):
        return handle_user_signup_with_referral(db=db, referred_user_id=referred_user_id, referral_code=referral_code)

@router.get("/invitation/{referral_code}")
def retrieve_invitation(referral_code: str, db: Session = Depends(get_db)):
        return get_invitation_by_referral_code(db=db, referral_code=referral_code)
