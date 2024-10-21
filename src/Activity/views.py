from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Header, UploadFile, File
from sqlmodel import Session
from src.database import get_db
from .models import Activity,ActivityCreate
from .service import create, get_all_activity, get_activity_by_token, update, delete_activity_by_token, get_all_activity_by_user_token

router = APIRouter()

@router.get("/get-all-activity")
def read_all_activity(db: Session = Depends(get_db), admin_token:str = Header(None, alias="AdminToken") , search:Optional[str] = None, story_id: Optional[str] = None):
    return get_all_activity(db=db, admin_token=admin_token, search=search, story_id=story_id)

@router.post("/create-activity")
def create_activity_details(activity_create: ActivityCreate, db: Session = Depends(get_db), admin_token:str = Header(None, alias="AdminToken")):
    return create(activity_create=activity_create, db=db, admin_token=admin_token)


# @router.post("/create-activity")
# async def create_activity_details(
#     activity_create: str = Depends(ActivityCreate),
#     db: Session = Depends(get_db),
#     admin_token: str = Header(None, alias="AdminToken"),
#     document_english: UploadFile = File(None)
# ):
#     return create(db=db, admin_token=admin_token, activity_create=activity_create, document_english=document_english)




@router.get("/get-activity-By-Token/{activity_id}")
def read_activity_by_token(activity_id:str, db: Session = Depends(get_db), user_token: str = Header(None, alias="UserToken")):
    return get_activity_by_token(activity_id=activity_id, db=db, user_token=user_token)

@router.get("/get-all-activity-By-user-Token")
def read_all_activity_by_user_token(db: Session = Depends(get_db), user_token: str = Header(None, alias="UserToken"), search:Optional[str] = None):
    return get_all_activity_by_user_token(db=db, user_token=user_token, search=search)


@router.put("/update-activity/{activity_id}")
def update_activity_details(activity_id:str, activity_update: ActivityCreate, db: Session = Depends(get_db), admin_token:str = Header(None, alias="AdminToken")):
    return update(activity_id=activity_id, activity_update=activity_update, db=db, admin_token=admin_token)


@router.delete("/delete-activity/{activity_id}")
def delete_activity_details_by_token(activity_id: str, db: Session = Depends(get_db), admin_token:str = Header(None, alias="AdminToken")):
    return delete_activity_by_token(activity_id=activity_id, db=db, admin_token=admin_token)