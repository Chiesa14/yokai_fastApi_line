from datetime import date

from sqlmodel import Session
from typing import List, Optional, Any, Dict
from .models import UserLogs, UserLogsCreate, UserLogsRead

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from ..UserProfile.models import UserProfile



def update_user_login_count(db: Session, user_id: int):
    today = date.today()

    # Check if the user exists
    user = db.query(UserProfile).filter(UserProfile.id == user_id).first()

    if not user:
        return {
            'status': 'false',
            'message': 'User does not exist.',
            'data': None
        }

    # Check if the user has a log entry
    user_log = db.query(UserLogs).filter(UserLogs.user_id == user_id).first()

    if user_log:
        # If the user logged in on the same day, do nothing
        if user_log.last_login_date == today:
            return {
                'status': 'true',
                'message': 'User already logged in today.',
                'data': user_log
            }
        else:
            # If the user logs in on a different day, increment the count
            user_log.login_count += 1
            user_log.last_login_date = today
            db.commit()
            db.refresh(user_log)

            return {
                'status': 'true',
                'message': 'User login count updated.',
                'data': user_log
            }
    else:
        # If it's the first time logging in, create a new log entry
        new_log = UserLogs(user_id=user_id, last_login_date=today)
        db.add(new_log)
        db.commit()
        db.refresh(new_log)

        return {
            'status': 'true',
            'message': 'User log created successfully.',
            'data': new_log
        }

def get_user_logs(db: Session, user_id: int, limit: Optional[int] = 100) -> dict[str, str] | Any:
    try:
        logs = db.query(UserLogs).filter(UserLogs.user_id == user_id).order_by(UserLogs.timestamp.desc()).limit(limit).all()
        return {
            'status': 'true',
            'message': 'User log retrieved successfully',
            'data': logs
        }
    except Exception as e:
        return {"status": "false", "message": f"An error occurred: {str(e)}"}

def get_all_user_logs(db: Session, limit: Optional[int] = 100) -> dict[str, str] | Any:
    try:
        logs = db.query(UserLogs).order_by(UserLogs.timestamp.desc()).limit(limit).all()
        return {
            'status': 'true',
            'message': 'All logs retrieved successfully',
            'data': logs
        }
    except Exception as e:
        return {"status": "false", "message": f"An error occurred: {str(e)}"}
