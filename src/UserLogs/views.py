from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from src.database import get_db
from .models import UserLogsCreate
from .service import  update_user_login_count, get_user_logs, get_all_user_logs
from typing import Optional

router = APIRouter()

@router.post("/create-user-log")
def create_log(user_log_request: UserLogsCreate,db: Session = Depends(get_db)):
    return update_user_login_count(db=db, user_id=user_log_request.user_id)

@router.get("/get-user-logs")
def get_logs(user_id: int, db: Session = Depends(get_db), limit: Optional[int] = 100):
        return get_user_logs(db=db, user_id=user_id, limit=limit)

@router.get("/get-all-user-logs")
def get_all_logs(db: Session = Depends(get_db), limit: Optional[int] = 100):
        return get_all_user_logs(db=db, limit=limit)
