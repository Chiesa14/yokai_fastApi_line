from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlmodel import Session
from src.database import get_db
from .models import ActivityDetails,ActivityDetailsCreate
from .service import create, get_all_activity_details, get_activity_deatils_by_token, update, delete_activity_details_by_token, get_all_activity_details_by_user_token, get_activities_and_details_by_chapter_id

router = APIRouter()

@router.get("/get-all-activity-details")
def read_all_activity_details(db: Session = Depends(get_db), admin_token:str = Header(None, alias="AdminToken") , search:Optional[str] = None):
    return get_all_activity_details(db=db, admin_token=admin_token, search=search)

@router.post("/create-activity-details")
def create_activity_details(activity_details_create: ActivityDetailsCreate, db: Session = Depends(get_db), admin_token:str = Header(None, alias="AdminToken")):
    return create(activity_details_create=activity_details_create, db=db, admin_token=admin_token)


@router.get("/get-activity-details-By-Token/{activity_id}")
def read_activity_by_token(activity_id:str, db: Session = Depends(get_db), user_token: str = Header(None, alias="UserToken")):
    return get_activity_deatils_by_token(activity_id=activity_id, db=db, user_token=user_token)

@router.get("/get-activities-by-chapter-id/{chapter_id}")
def read_activities_and_details_by_chapter_id(chapter_id:str, db: Session = Depends(get_db), user_token: str = Header(None, alias="UserToken")):
    return get_activities_and_details_by_chapter_id(chapter_id=chapter_id, db=db, user_token=user_token)

@router.get("/get-all-activity-details-By-user-Token")
def read_all_activity_by_user_token(db: Session = Depends(get_db), user_token: str = Header(None, alias="UserToken"), search:Optional[str] = None):
    return get_all_activity_details_by_user_token(db=db, user_token=user_token, search=search)


@router.put("/update-activity-details/{activity_details_id}")
def update_activity_details(activity_details_id:str, activity_details_update: ActivityDetailsCreate, db: Session = Depends(get_db), admin_token:str = Header(None, alias="AdminToken")):
    return update(activity_details_id=activity_details_id, activity_details_update=activity_details_update, db=db, admin_token=admin_token)


@router.delete("/delete-activity-details/{activity_details_id}")
def delete_activity_details(activity_details_id: str, db: Session = Depends(get_db), admin_token:str = Header(None, alias="AdminToken")):
    return delete_activity_details_by_token(activity_details_id=activity_details_id, db=db, admin_token=admin_token)