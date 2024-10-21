from .models import Stories, StoriesCreate
from typing import List, Optional
from sqlmodel import Session
from datetime import datetime, timedelta
from fastapi import status, HTTPException
from src.parameter import jwt, SECRET_KEY, ALGORITHM
from src.UserProfile.models import UserProfile
from src.Chapter.models import Chapter
from src.Activity.models import Activity
from sqlalchemy import func
from src.Character.models import Character
from src.ChapterWiseUser.models import ChapterWiseUser


# def get_all_stories(db: Session, admin_token: str, search:Optional[str] = None):
#     try:
#         # Decrypt the token
#         decrypted_token = decrypt_token(admin_token.encode(), fernet_key)

#         # Decode the JWT token
#         payload = jwt.decode(
#             decrypted_token, jwt_secret_key, algorithms=["HS256"])

#         # Extract user_id from the payload
#         user_id = payload.get('user_id')

#         # Retrieve user data from the database using the user_id
#         user_data = db.query(UserProfile).filter(
#             UserProfile.id == user_id).first()

#         if not user_data:
#             return {"status": 'false', 'message': "User not found"}

#         # Check if the user is an admin
#         if user_data.email != 'admin@gmail.com':
#             return {"status": 'false', 'message': "Access denied"}

#         all_stories_query = db.query(Stories)

#         if search is not None:
#            all_stories_query = all_stories_query.filter(Stories.name.ilike(f"%{search}%"))

#         all_stories = all_stories_query.order_by(Stories.id.desc()).all()
        
#         response = {
#             'status': 'true',
#             'message': "Data Received Successfully",
#             'data': all_stories
#         }
#         return response

#     except jwt.ExpiredSignatureError:
#         return {"status": "false", "message": "Token has expired"}
#     except jwt.InvalidTokenError:
#         return {"status": "false", "message": "Invalid token"}
#     except InvalidToken:
#         return {"status": "false", "message": "Invalid or corrupted token"}

def get_all_stories(db: Session, admin_token: str, search: Optional[str] = None):
    try:
        # Decode the JWT token
        payload = jwt.decode(admin_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        role = payload.get("role")

        # Retrieve user data from the database using the user_id
        user_data = db.query(UserProfile).filter(
            UserProfile.id == user_id).first()

        if not user_data:
            return {"status": 'false', 'message': "User not found"}

        # Verify that the user is an admin
        if role != "admin":
            return {"status": 'false', 'message': "Access denied"}

        # Query all stories
        all_stories_query = db.query(Stories)

        if search is not None:
            all_stories_query = all_stories_query.filter(Stories.name.ilike(f"%{search}%"))

        all_stories = all_stories_query.order_by(Stories.id.desc()).all()

        # Prepare response with additional counts
        response_data = []
        for story in all_stories:
            # Count chapters related to the story
            chapter_count = db.query(func.count(Chapter.id)).filter(Chapter.stories_id == story.id).scalar()

            # Count activities related to the story's chapters
            activity_count = db.query(func.count(Activity.id)).\
                join(Chapter, Activity.chapter_id == Chapter.id).\
                filter(Chapter.stories_id == story.id).scalar()

            # Construct story data with additional counts
            story_data = {
                'id': story.id,
                'name': story.name,
                'description': story.discription,  # Adjust as per your actual column name
                'stories_image': story.stories_image,  # Adjust as per your actual column name
                'created_at': story.created_at,
                'updated_at': story.updated_at,
                'chapter_count': chapter_count,
                'activity_count': activity_count
            }
            response_data.append(story_data)

        response = {
            'status': 'true',
            'message': "Data Received Successfully",
            'data': response_data
        }
        return response

    except jwt.InvalidTokenError:
        return {"status": "false", "message": "Invalid token"}
    except Exception as e:
        return {"status": "false", "message": f"An error occurred: {str(e)}"}



def create(stories_create: StoriesCreate, db: Session, admin_token:str):
    try:
        # Decode the JWT token
        payload = jwt.decode(admin_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        role = payload.get("role")

        # Retrieve user data from the database using the user_id
        user_data = db.query(UserProfile).filter(
            UserProfile.id == user_id).first()

        if not user_data:
            return {"status": 'false', 'message': "User not found"}

        # Verify that the user is an admin
        if role != "admin":
            return {"status": 'false', 'message': "Access denied"}

        db_stories = Stories(**stories_create.dict())
        db.add(db_stories)
        db.commit()
        db.refresh(db_stories)
        response = {'status': 'true',
                'message': 'Stories Details Added Successfully', 'data': db_stories}

        return response

    except jwt.InvalidTokenError:
        return {"status": "false", "message": "Invalid token"}
    except Exception as e:
        return {"status": "false", "message": f"An error occurred: {str(e)}"}


def update(stories_id: str, stories_update: Stories, db: Session, admin_token: str):
    try:
        # Decode the JWT token
        payload = jwt.decode(admin_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        role = payload.get("role")

        # Retrieve user data from the database using the user_id
        user_data = db.query(UserProfile).filter(
            UserProfile.id == user_id).first()

        if not user_data:
            return {"status": 'false', 'message': "User not found"}

        # Verify that the user is an admin
        if role != "admin":
            return {"status": 'false', 'message': "Access denied"}

        # Prepare the update data
        db_stories_update = stories_update.dict(exclude_unset=True)
        # Update user profile in the database
        db.query(Stories).filter(Stories.id ==
                                 stories_id).update(db_stories_update)
        db.commit()

        response = {
            'status': 'true',
            'message': "Stories Details Updated Successfully",
            'data': db_stories_update
        }
        return response

    except jwt.InvalidTokenError:
        return {"status": "false", "message": "Invalid token"}
    except Exception as e:
        return {"status": "false", "message": f"An error occurred: {str(e)}"}


def get_stories_by_token(stories_id: str, db: Session, user_token: str):
    try:
        # Decode the JWT token
        payload = jwt.decode(user_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")

        user_data = db.query(UserProfile).filter(
            UserProfile.id == user_id).first()

        if not user_data:
            return {"status": 'false', 'message': "User not found"}

        # Retrieve user data from the database using the user_id
        stories_data = db.query(Stories).filter(
            Stories.id == stories_id).first()
        
        if not stories_data:
            return {"status": 'false', 'message': "Stories not found"}
        
        chapter_count = db.query(Chapter).filter(Chapter.stories_id == stories_id).count()
        
        activity_count = db.query(Activity).filter(Activity.story_id == stories_id).count()
        
        charcter = db.query(Character).filter(Character.stories_id == stories_id).first()
        
        if not charcter :
            charcter_name = None
            charcter_image = None
        else :
            charcter_name = charcter.name
            charcter_image = charcter.character_image    

        return {
            'status': 'true',
            'message': 'User data retrieved successfully',
            'data': {
                'name': stories_data.name,
                'discription': stories_data.discription,
                'stories_image': stories_data.stories_image,
                'chapter_count' : chapter_count,
                'activity_count' : activity_count,
                'charcter' : charcter_name,
                'charcter_image': charcter_image,
                'created_at': stories_data.created_at,
                'updated_at': stories_data.updated_at
            }
        }
    except jwt.InvalidTokenError:
        return {"status": "false", "message": "Invalid token"}
    except Exception as e:
        return {"status": "false", "message": f"An error occurred: {str(e)}"}
    
def get_all_stories_by_user_token(db: Session, user_token: str, search:Optional[str] = None):
    try:
        # Decode the JWT token
        payload = jwt.decode(user_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")

        user_data = db.query(UserProfile).filter(
            UserProfile.id == user_id).first()

        if not user_data:
            return {"status": 'false', 'message': "User not found"}
        
        all_stories_query = db.query(Stories)

        if search is not None:
           all_stories_query = all_stories_query.filter(Stories.name.ilike(f"%{search}%"))

        all_stories = all_stories_query.order_by(Stories.id.desc()).all()

        return {
            'status': 'true',
            'message': 'User data retrieved successfully',
            'data': all_stories
        }
    except jwt.InvalidTokenError:
        return {"status": "false", "message": "Invalid token"}
    except Exception as e:
        return {"status": "false", "message": f"An error occurred: {str(e)}"}    


def delete_stories_by_token(stories_id: str, db: Session, admin_token: str):
    try:
        # Decode the JWT token
        payload = jwt.decode(admin_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        role = payload.get("role")

        # Retrieve user data from the database using the user_id
        user_data = db.query(UserProfile).filter(
            UserProfile.id == user_id).first()

        if not user_data:
            return {"status": 'false', 'message': "User not found"}

        # Verify that the user is an admin
        if role != "admin":
            return {"status": 'false', 'message': "Access denied"}
        
        stories_details = db.query(Stories).filter(
            Stories.id == stories_id).first()
        
        if not stories_details:
            return {"status": 'false', 'message': "Stories not found"}
        
        db.query(Chapter).filter(Chapter.stories_id == stories_id).delete()
        
        db.query(Character).filter(Character.stories_id == stories_id).delete()
        
        db.query(ChapterWiseUser).filter(ChapterWiseUser.stories_id == stories_id).delete()

        db.delete(stories_details)
        db.commit()

        response = {
            'status': 'true',
            'message': "Stories Details deleted successfully"
        }

        return response

    except jwt.InvalidTokenError:
        return {"status": "false", "message": "Invalid token"}
    except Exception as e:
        return {"status": "false", "message": f"An error occurred: {str(e)}"}
