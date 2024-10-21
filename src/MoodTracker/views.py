from typing import List

from fastapi import APIRouter, Depends
from sqlmodel import Session
from src.database import get_db
from .service import create_mood, get_all_mood_gifs_by_user
from .models import MoodCreate, MoodUpdate, Mood

router = APIRouter()

@router.post("/moods")
def create_mood_api(mood_create: MoodCreate, db: Session = Depends(get_db)):
    return create_mood(db=db, mood_create=mood_create)

@router.get("/moods/user/{user_id}")
def get_mood_gifs(user_id: int, db: Session = Depends(get_db)):
    return get_all_mood_gifs_by_user(db, user_id)