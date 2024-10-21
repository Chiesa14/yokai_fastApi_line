from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlmodel import Session
from src.database import get_db
from src.Stories.models import Stories,StoriesCreate
from src.Stories.service import create, get_all_stories, get_stories_by_token, update, delete_stories_by_token, get_all_stories_by_user_token

router = APIRouter()

@router.get("/get-all-stories")
def read_all_stories_details(db: Session = Depends(get_db), admin_token:str = Header(None, alias="AdminToken") , search:Optional[str] = None):
    return get_all_stories(db=db, admin_token=admin_token, search=search)

@router.post("/create-stories")
def create_stories_details(stories_create: StoriesCreate, db: Session = Depends(get_db), admin_token:str = Header(None, alias="AdminToken")):
    return create(stories_create=stories_create, db=db, admin_token=admin_token)


@router.get("/get-stories-By-Token/{stories_id}")
def read_stories_by_token(stories_id:str, db: Session = Depends(get_db), user_token: str = Header(None, alias="UserToken")):
    return get_stories_by_token(stories_id=stories_id, db=db, user_token=user_token)

@router.get("/get-all-stories-By-user-Token")
def read_all_stories_by_user_token(db: Session = Depends(get_db), user_token: str = Header(None, alias="UserToken"), search:Optional[str] = None):
    return get_all_stories_by_user_token(db=db, user_token=user_token, search=search)


@router.put("/update-stories/{stories_id}")
def update_stories_details(stories_id:str, stories_update: StoriesCreate, db: Session = Depends(get_db), admin_token:str = Header(None, alias="AdminToken")):
    return update(stories_id=stories_id, stories_update=stories_update, db=db, admin_token=admin_token)


@router.delete("/delete-stories/{stories_id}")
def delete_stories_details_by_token(stories_id: str, db: Session = Depends(get_db), admin_token:str = Header(None, alias="AdminToken")):
    return delete_stories_by_token(stories_id=stories_id, db=db, admin_token=admin_token)