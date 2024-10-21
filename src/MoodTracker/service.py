from operator import and_

import pytz
from fastapi import HTTPException, status
from sqlalchemy import func
from sqlmodel import Session, select
from typing import List
from .models import Mood, MoodCreate, MoodUpdate

from sqlmodel import Session
from .models import MoodCreate, Mood  # Adjust the import as per your project structure


from datetime import datetime, date

india_tz = pytz.timezone('Asia/Kolkata')


def create_mood(db: Session, mood_create: MoodCreate):
    # Validate user_id
    if not mood_create.user_id:
        return {'status': 'false', 'message': 'User ID is required.'}

    # Validate mood_level
    if mood_create.mood_level < 0 or mood_create.mood_level > 1:
        return {'status': 'false', 'message': 'Mood level must be between 0 and 1.'}

    # Validate mood_gif
    if mood_create.mood_gif < 0 or mood_create.mood_gif > 5:
        return {'status': 'false', 'message': 'Mood GIF must be between 0 and 5.'}

    # Get today's date in India timezone
    now_in_india = datetime.now(india_tz)
    today = func.date(now_in_india)

    # Check if there's an existing mood for today
    existing_mood = db.query(Mood).filter(
        and_(
            Mood.user_id == mood_create.user_id,
            func.date(Mood.date) == today
        )
    ).first()

    if existing_mood:
        existing_mood.mood_gif = mood_create.mood_gif
        existing_mood.mood_level = mood_create.mood_level
        existing_mood.updated_at = now_in_india
        db.commit()
        db.refresh(existing_mood)
        response = {
            'status': 'true',
            'message': "Today's mood updated successfully",
            'data': existing_mood
        }
    else:
        db_mood = Mood(**mood_create.dict())
        db_mood.created_at = now_in_india
        db.add(db_mood)
        db.commit()
        db.refresh(db_mood)
        response = {
            'status': 'true',
            'message': "Today's mood added successfully",
            'data': db_mood
        }

    return response
def get_all_mood_gifs_by_user(db: Session, user_id: int):
    # Check if a user ID is provided
    if not user_id:
        return {'status': 'false', 'message': 'User ID is required.'}

    # Query the database for all mood entries by user_id
    mood_entries = db.query(Mood).filter(Mood.user_id == user_id).all()

    # If no mood entry exists for this user, return an error message
    if not mood_entries:
        return {'status': 'false', 'message': f'No mood entries found for user ID {user_id}'}

    # Extract mood_gif and other relevant data from all mood entries
    mood_gifs = [
        {
            'mood_gif': mood.mood_gif,
            'mood_level': mood.mood_level,
            'date': mood.date
        }
        for mood in mood_entries
    ]

    response = {
        'status': 'true',
        'message': f'{len(mood_entries)} Mood GIFs Retrieved Successfully',
        'data': mood_gifs
    }
    return response

def get_mood_by_id(db: Session, mood_id: int):
    mood = db.get(Mood, mood_id)
    if not mood:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Mood with id {mood_id} not found"
        )
    return mood

def get_all_moods(db: Session, skip: int = 0, limit: int = 10) -> List[Mood]:
    return db.exec(select(Mood).offset(skip).limit(limit)).all()

def update_mood(db: Session, mood_id: int, mood_update: MoodUpdate):
    mood = get_mood_by_id(db, mood_id)
    if mood_update.mood_type:
        mood.mood_type = mood_update.mood_type
    if mood_update.description:
        mood.description = mood_update.description
    db.add(mood)
    db.commit()
    db.refresh(mood)
    return mood

def delete_mood(db: Session, mood_id: int):
    mood = get_mood_by_id(db, mood_id)
    db.delete(mood)
    db.commit()
    return {"status": "success", "message": f"Mood {mood_id} deleted successfully"}
