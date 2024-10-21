from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlmodel import Session
from src.database import get_db
from src.Chapter.models import Chapter, ChapterCreate
from src.Chapter.service import create, get_chapter_by_storie_id, get_chapter_by_token, update, delete_chapter_by_token

router = APIRouter()

@router.get("/get-chapter-by-stories")
def read_chapter_by_storie_id(stories_id:Optional[str]=None, db: Session = Depends(get_db), user_token:str = Header(None, alias="UserToken"), search:Optional[str] = None):
    return get_chapter_by_storie_id(stories_id=stories_id, db=db, user_token=user_token, search=search)

@router.post("/create-chapter")
def create_chapter_details(chapter_create: ChapterCreate, db: Session = Depends(get_db), admin_token:str = Header(None, alias="AdminToken")):
    return create(chapter_create=chapter_create, db=db, admin_token=admin_token)


@router.get("/get-chapter-By-Token/{chapter_id}")
def raed_chapter_by_token(chapter_id:str, db: Session = Depends(get_db), user_token:str = Header(None, alias="UserToken")):
    return get_chapter_by_token(chapter_id=chapter_id, db=db, user_token=user_token)


@router.put("/update-chapter/{chapter_id}")
def update_stories_details(chapter_id:str, chapter_update: ChapterCreate, db: Session = Depends(get_db), admin_token:str = Header(None, alias="AdminToken")):
    return update(chapter_id=chapter_id, chapter_update=chapter_update, db=db, admin_token=admin_token)


@router.delete("/delete-chapter/{chapter_id}")
def delete_chapter_details_by_token(chapter_id: str, db: Session = Depends(get_db), admin_token:str = Header(None, alias="AdminToken")):
    return delete_chapter_by_token(chapter_id=chapter_id, db=db, admin_token=admin_token)