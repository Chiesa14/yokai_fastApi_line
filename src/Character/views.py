from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlmodel import Session
from src.database import get_db
from .models import Character,CharacterCreate
from .service import create, get_all_character, update, delete_character_by_token, get_character_by_id, get_all_character_by_user, get_character_by_user,get_locked_characters_for_user,get_unlocked_characters_for_user

router = APIRouter()

@router.get("/get-all-character")
def read_all_character(db: Session = Depends(get_db), admin_token:str = Header(None, alias="AdminToken") , search:Optional[str] = None):
    return get_all_character(db=db, admin_token=admin_token, search=search)

@router.get("/get-all-character-by-user")
def read_all_character_by_user(db: Session = Depends(get_db), user_token:str = Header(None, alias="UserToken") , search:Optional[str] = None):
    return get_all_character_by_user(db=db, user_token=user_token, search=search)

@router.post("/create-character")
def create_character(character_create: CharacterCreate, db: Session = Depends(get_db), admin_token:str = Header(None, alias="AdminToken")):
    return create(character_create=character_create, db=db, admin_token=admin_token)


@router.get("/get-character-by-id/{character_id}")
def read_character_by_id(character_id:str, db: Session = Depends(get_db), admin_token: str = Header(None, alias="AdminToken")):
    return get_character_by_id(db=db, admin_token=admin_token, character_id=character_id)

@router.get("/get-character-by-user/{character_id}")
def read_character_by_user(character_id:str, db: Session = Depends(get_db), user_token: str = Header(None, alias="UserToken")):
    return get_character_by_user(db=db, user_token=user_token, character_id=character_id)

@router.put("/update-character/{character_id}")
def update_character(character_id:str, character_update: CharacterCreate, db: Session = Depends(get_db), admin_token:str = Header(None, alias="AdminToken")):
    return update(character_id=character_id, character_update=character_update, db=db, admin_token=admin_token)


@router.delete("/delete-character/{character_id}")
def delete_activity_details(character_id: str, db: Session = Depends(get_db), admin_token:str = Header(None, alias="AdminToken")):
    return delete_character_by_token(character_id=character_id, db=db, admin_token=admin_token)

@router.get("/get-locked-character-by-user")
def read_locked_characters_for_user(db: Session = Depends(get_db), search: Optional[str] = None, user_token: str = Header(None, alias="UserToken")):
    return get_locked_characters_for_user(db=db, user_token=user_token, search=search)

@router.get("/get-unlocked-character-by-user")
def read_unlocked_characters_for_user(db: Session = Depends(get_db), search: Optional[str] = None, user_token: str = Header(None, alias="UserToken")):
    return get_unlocked_characters_for_user(db=db, user_token=user_token, search=search)