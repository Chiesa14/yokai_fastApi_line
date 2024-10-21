from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlmodel import Session
from src.database import get_db
from .models import ChapterWiseUser, ChapterWiseUserCreate, UpdateReadStatus
from .service import add_chapters_for_all_users, get_chapters_by_stories_id_for_user,update_read_status,get_latest_chapters_by_user

router = APIRouter()

@router.post("/add-chapters-for-all-users")
def create_chapters_for_all_users(db: Session = Depends(get_db)):
    return add_chapters_for_all_users(db=db)

@router.get("/get-chapters-by-stories-id-for-user")
def read_chapters_by_stories_id_for_user(stories_id:Optional[str] = None, db: Session = Depends(get_db), search: Optional[str] = None, user_token: str = Header(None, alias="UserToken")):
    return get_chapters_by_stories_id_for_user(stories_id=stories_id, db=db, user_token=user_token, search=search)

@router.get("/get-latest-read-chapter-by-user")
def read_latest_chapters_by_user(db: Session = Depends(get_db), user_token: str = Header(None, alias="UserToken")):
    return get_latest_chapters_by_user(db=db, user_token=user_token)

@router.put("/update-read-status/{chapter_id}")
def update_read_status_route(chapter_id: str, read_data: UpdateReadStatus,db: Session = Depends(get_db), user_token: str = Header(None, alias="UserToken")):
    return update_read_status(user_token=user_token, chapter_id=chapter_id, read_data=read_data, db=db)