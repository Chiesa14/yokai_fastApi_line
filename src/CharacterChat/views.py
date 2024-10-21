from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlmodel import Session
from src.database import get_db
from .models import CharacterChat,CharacterChatCreate
from .service import create, get_character_chat_by_user

router = APIRouter()

@router.post("/create-user-character-chat")
def create_user_character_chat(character_chat_create: CharacterChatCreate, db: Session = Depends(get_db), user_token: str = Header(None, alias="UserToken")):
    return create(db=db, character_chat_create=character_chat_create, user_token=user_token)

@router.get("/get-user-character-chat")
def read_character_chat_by_user(character_id: str, db: Session = Depends(get_db), page_number: Optional[str] = None, user_token: str = Header(None, alias="UserToken")):
    return get_character_chat_by_user(user_token=user_token, character_id=character_id, db=db, page_number=page_number)