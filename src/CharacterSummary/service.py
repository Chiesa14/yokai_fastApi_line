from .models import UserSummary,UserSummaryCreate
from typing import List, Optional
from sqlmodel import Session
from datetime import datetime, timedelta
from fastapi import status, HTTPException
from src.parameter import jwt, SECRET_KEY, ALGORITHM
from typing import Optional
from sqlalchemy.orm import Session
import jwt
from src.UserProfile.models import UserProfile
import pytz

india_tz = pytz.timezone('Asia/Kolkata')
# Get the current time in the specified timezone
now = datetime.now(india_tz)

def create(db: Session, user_token:str, user_summary_create: UserSummaryCreate):
        
    try:
        # Decode the JWT token
        payload = jwt.decode(user_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")

        # Retrieve user data from the database using the user_id
        user_data = db.query(UserProfile).filter(
            UserProfile.id == user_id).first()

        if not user_data:
            return {"status": 'false', 'message': "User not found"}

        existing_summary = db.query(UserSummary).filter(UserSummary.user_id == user_id, UserSummary.character_id == user_summary_create.character_id).first()
    
        if existing_summary:
            for key, value in user_summary_create.dict().items():
                setattr(existing_summary, key, value)    
            existing_summary.updated_at = now
            existing_summary.user_id = user_id        

            db.commit()
            db.refresh(existing_summary)
            response = {'status': 'true', 'message': 'User Summary Details Updated Successfully', 'data': existing_summary}
            return response
        else:
            # Create a new entry since it doesn't exist
            user_summary_create.user_id = user_id
            db_user_summary_create = UserSummary(**user_summary_create.dict())
            db.add(db_user_summary_create)
            db.commit()
            db.refresh(db_user_summary_create)
            response = {'status': 'true', 'message': ' User Summary Details Added Successfully', 'data': db_user_summary_create}
            return response  

    except jwt.InvalidTokenError:
        return {"status": "false", "message": "Invalid token"}
    except Exception as e:
        return {"status": "false", "message": f"An error occurred: {str(e)}"}