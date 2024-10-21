from .models import Usercharacter, UsercharacterCreate
from typing import List, Optional
from sqlmodel import Session
from datetime import datetime, timedelta
from fastapi import status, HTTPException
from src.parameter import jwt, SECRET_KEY, ALGORITHM
from src.UserProfile.models import UserProfile
from src.Stories.models import Stories
from typing import Optional
from sqlalchemy.orm import Session
import jwt

def create(user_character_create: UsercharacterCreate, db: Session, user_token: str):
    try:
        # Decode the JWT token
        payload = jwt.decode(user_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")

        user_data = db.query(UserProfile).filter(
            UserProfile.id == user_id).first()

        if not user_data:
            return {"status": 'false', 'message': "User not found"}

        character_id = user_character_create.character_id

        existing_story = db.query(Usercharacter).filter(
            Usercharacter.user_id == user_id, Usercharacter.character_id == character_id).all()
        if len(existing_story) > 0:
            return {'status': 'false', 'message': 'This Character is already Unlocked.'}
 
        user_character_create.user_id = user_id
        db_user_character = Usercharacter(**user_character_create.dict())
        db.add(db_user_character)
        db.commit()
        db.refresh(db_user_character)
        response = {'status': 'true',
                    'message': 'Character Added Successfully', 'data': db_user_character}

        return response

    except jwt.InvalidTokenError:
        return {"status": "false", "message": "Invalid token"}
    except Exception as e:
        return {"status": "false", "message": f"An error occurred: {str(e)}"}