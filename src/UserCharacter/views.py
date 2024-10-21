from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlmodel import Session
from src.database import get_db
from .models import Usercharacter,UsercharacterCreate
from .service import create

router = APIRouter()

@router.post("/create-user-character")
def create_user_character(user_character_create: UsercharacterCreate, db: Session = Depends(get_db), user_token: str = Header(None, alias="UserToken")):
    return create(user_character_create=user_character_create, db=db, user_token=user_token)