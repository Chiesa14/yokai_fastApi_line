from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Header, Body
from sqlmodel import Session
from src.database import get_db
from .models import UserSummaryCreate
from .service import create
from typing import Optional

router = APIRouter()

@router.post("/create-user-summary")
def create_user_summary(user_summary_create: UserSummaryCreate, db: Session = Depends(get_db), user_token: str = Header(None, alias="UserToken")):
    return create(db=db, user_token=user_token, user_summary_create=user_summary_create)

