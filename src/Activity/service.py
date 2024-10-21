from .models import Activity, ActivityCreate
from typing import List, Optional
from sqlmodel import Session
from datetime import datetime, timedelta
from fastapi import status, HTTPException, UploadFile
from src.parameter import  jwt, SECRET_KEY, ALGORITHM
from src.UserProfile.models import UserProfile
from src.Stories.models import Stories
from src.Chapter.models import Chapter
import csv
from src.ActivityDetails.models import ActivityDetails
from sqlalchemy import func

# def get_all_activity(db: Session, admin_token: str, search: Optional[str] = None):
#     try:
#         # Decrypt the token
#         decrypted_token = decrypt_token(admin_token.encode(), fernet_key)

#         # Decode the JWT token
#         payload = jwt.decode(decrypted_token, jwt_secret_key, algorithms=["HS256"])

#         # Extract user_id from the payload
#         user_id = payload.get('user_id')

#         # Retrieve user data from the database using the user_id
#         user_data = db.query(UserProfile).filter(UserProfile.id == user_id).first()

#         if not user_data:
#             return {"status": 'false', 'message': "User not found"}

#         # Check if the user is an admin
#         if user_data.email != 'admin@gmail.com':
#             return {"status": 'false', 'message': "Access denied"}

#         all_activity_query = db.query(
#             Activity,
#             Stories.name.label('story_name'),
#             Chapter.name.label('chapter_name'),
#             Chapter.chapter_no.label('chapter_no')
#         ).join(Stories, Activity.story_id == Stories.id).join(Chapter, Activity.chapter_id == Chapter.id)

#         if search is not None:
#             all_activity_query = all_activity_query.filter(Activity.title.ilike(f"%{search}%"))

#         all_activity = all_activity_query.order_by(Activity.id.desc()).all()

#         # Format the response
#         activities = []
#         for activity, story_name, chapter_name, chapter_no in all_activity:
#             activities.append({
#                 'id': activity.id,
#                 'story_id': activity.story_id,
#                 'story_name': story_name,
#                 'chapter_id': activity.chapter_id,
#                 'chapter_no': chapter_no,
#                 'chapter_name': chapter_name,
#                 'title': activity.title,
#                 'time': activity.time,
#                 'short_discription': activity.short_discription,
#                 'activity_image': activity.activity_image,
#                 'document_english': activity.document_english,
#                 'document_japanese': activity.document_japanese,
#                 'created_at': activity.created_at,
#                 'updated_at': activity.updated_at
#             })

#         response = {
#             'status': 'true',
#             'message': "Data Received Successfully",
#             'data': activities
#         }
#         return response

#     except jwt.ExpiredSignatureError:
#         return {"status": "false", "message": "Token has expired"}
#     except jwt.InvalidTokenError:
#         return {"status": "false", "message": "Invalid token"}
#     except InvalidToken:
#         return {"status": "false", "message": "Invalid or corrupted token"}

def get_all_activity(db: Session, admin_token: str, search: Optional[str] = None, story_id: Optional[str] = None):
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

        # Build the initial query
        all_activity_query = db.query(
            Activity,
            Stories.name.label('story_name'),
            Chapter.name.label('chapter_name'),
            Chapter.chapter_no.label('chapter_no')
        ).join(Stories, Activity.story_id == Stories.id).join(Chapter, Activity.chapter_id == Chapter.id)

        # Filter by story_id if provided
        if story_id is not None:
            all_activity_query = all_activity_query.filter(Activity.story_id == story_id)

        # Filter by search term if provided
        if search is not None:
            all_activity_query = all_activity_query.filter(Activity.title.ilike(f"%{search}%"))

        # Fetch all activities ordered by id descending
        all_activity = all_activity_query.order_by(Activity.id.desc()).all()

        # Format the response
        activities = []
        for activity, story_name, chapter_name, chapter_no in all_activity:
            activities.append({
                'id': activity.id,
                'story_id': activity.story_id,
                'story_name': story_name,
                'chapter_id': activity.chapter_id,
                'chapter_no': chapter_no,
                'chapter_name': chapter_name,
                'title': activity.title,
                'time': activity.time,
                'short_discription': activity.short_description,
                'activity_image': activity.activity_image,
                'document_english': activity.document_english,
                'document_japanese': activity.document_japanese,
                'image': activity.image,
                'audio': activity.audio,
                'end_image': activity.end_image,
                'created_at': activity.created_at,
                'updated_at': activity.updated_at
            })

        response = {
            'status': 'true',
            'message': "Data Received Successfully",
            'data': activities
        }
        return response

    except jwt.InvalidTokenError:
        return {"status": "false", "message": "Invalid token"}
    except Exception as e:
        return {"status": "false", "message": f"An error occurred: {str(e)}"}


def create(activity_create: ActivityCreate, db: Session, admin_token:str):
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
        
        chapter_id = activity_create.chapter_id
        
        existing_activity = db.query(Activity).filter(Activity.chapter_id == chapter_id).first()
        
        if existing_activity:
            return {
                'status': 'false',
                'message': 'This Chapter Activity is already added.'
        }

        db_activity = Activity(**activity_create.dict())
        db.add(db_activity)
        db.commit()
        db.refresh(db_activity)
        
        response = {'status': 'true',
                'message': 'Activity Added Successfully', 'data': db_activity}

        return response

    except jwt.InvalidTokenError:
        return {"status": "false", "message": "Invalid token"}
    except Exception as e:
        return {"status": "false", "message": f"An error occurred: {str(e)}"}

# async def create(db: Session, admin_token: str, activity_create: ActivityCreate, document_english: UploadFile = None):
#     try:
#         # Decrypt the token
#         decrypted_token = decrypt_token(admin_token.encode(), fernet_key)

#         # Decode the JWT token
#         payload = jwt.decode(decrypted_token, jwt_secret_key, algorithms=["HS256"])

#         # Extract user_id from the payload
#         user_id = payload.get('user_id')

#         user_data = db.query(UserProfile).filter(UserProfile.id == user_id).first()

#         if not user_data:
#             return {"status": 'false', 'message': "User not found"}

#         # Check if the user is an admin
#         if user_data.email != 'admin@gmail.com':
#             return {"status": 'false', 'message': "Access denied"}

#         chapter_id = activity_create.chapter_id

#         existing_activity = db.query(Activity).filter(Activity.chapter_id == chapter_id).first()

#         if existing_activity:
#             return {'status': 'false', 'message': 'This Chapter Activity is already added.'}

#         db_activity = Activity(**activity_create.dict())
#         db.add(db_activity)
#         db.commit()
#         db.refresh(db_activity)

#         # Process CSV file if provided
#         if document_english is not None:
#             # Assuming document_english is a CSV file
#             csv_data = document_english.file.read().decode("utf-8").splitlines()
#             csv_reader = csv.DictReader(csv_data)

#             activity_id = db_activity.id  # Assuming db_activity has activity_id

#             # Determine the next sr_no
#             next_sr_no = db.query(func.max(ActivityDetails.sr_no)).filter(ActivityDetails.activity_id == activity_id).scalar() or 0
#             next_sr_no += 1

#             for row in csv_reader:
#                 # Extract data from CSV row
#                 question = row.get('Questions')
#                 options = row.get('Options').split(',')

#                 # Ensure the options list has at least 4 elements
#                 if len(options) < 4:
#                     return {"status": "false", "message": "Options field must have at least 4 options"}

#                 option_a = options[0]
#                 option_b = options[1]
#                 option_c = options[2]
#                 option_d = options[3]
#                 correct_answer = row.get('correct_answer')
#                 explanation = row.get('explanation')

#                 # Create ActivityDetails object
#                 activity_detail = ActivityDetails(
#                     activity_id=activity_id,
#                     sr_no=next_sr_no,
#                     question=question,
#                     option_a=option_a,
#                     option_b=option_b,
#                     option_c=option_c,
#                     option_d=option_d,
#                     correct_answer=correct_answer,
#                     explanation=explanation
#                 )

#                 db.add(activity_detail)
#                 next_sr_no += 1  # Increment sr_no for the next detail

#         db.commit()

#         response = {'status': 'true', 'message': 'Activity Added Successfully', 'data': db_activity}

#         return response

#     except jwt.ExpiredSignatureError:
#         return {"status": "false", "message": "Token has expired"}
#     except jwt.InvalidTokenError:
#         return {"status": "false", "message": "Invalid token"}
#     except InvalidToken:
#         return {"status": "false", "message": "Invalid or corrupted token"}


def update(activity_id: str, activity_update: Activity, db: Session, admin_token: str):
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
        db_activity_update = activity_update.dict(exclude_unset=True)
        # Update user profile in the database
        db.query(Activity).filter(Activity.id ==
                                 activity_id).update(db_activity_update)
        db.commit()

        response = {
            'status': 'true',
            'message': "Activity Updated Successfully",
            'data': db_activity_update
        }
        return response

    except jwt.InvalidTokenError:
        return {"status": "false", "message": "Invalid token"}
    except Exception as e:
        return {"status": "false", "message": f"An error occurred: {str(e)}"}


def get_activity_by_token(activity_id: str, db: Session, user_token: str):
    try:
        # Decode the JWT token
        payload = jwt.decode(user_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")

        user_data = db.query(UserProfile).filter(
            UserProfile.id == user_id).first()

        if not user_data:
            return {"status": 'false', 'message': "User not found"}

        # Retrieve user data from the database using the user_id
        activity_data = db.query(Activity).filter(
            Activity.id == activity_id).first()
        
        if not activity_data:
            return {"status": 'false', 'message': "Activitiy not found"}

        return {
            'status': 'true',
            'message': 'Activity data retrieved successfully',
            'data': {
                'id': activity_data.id,
                'story_id': activity_data.story_id,
                'chapter_id': activity_data.chapter_id,
                'title': activity_data.title,
                'time': activity_data.time,
                'short_discription': activity_data.short_description,
                'activity_image': activity_data.activity_image,
                'document_english': activity_data.document_english,
                'document_japanese': activity_data.document_japanese,
                'image': activity_data.image,
                'audio': activity_data.audio,
                'end_image': activity_data.end_image,
                'created_at': activity_data.created_at,
                'updated_at': activity_data.updated_at
            }
        }
    except jwt.InvalidTokenError:
        return {"status": "false", "message": "Invalid token"}
    except Exception as e:
        return {"status": "false", "message": f"An error occurred: {str(e)}"}
    
def get_all_activity_by_user_token(db: Session, user_token: str, search:Optional[str] = None):
    try:
        # Decode the JWT token
        payload = jwt.decode(user_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")

        user_data = db.query(UserProfile).filter(
            UserProfile.id == user_id).first()

        if not user_data:
            return {"status": 'false', 'message': "User not found"}
        
        all_activity_query = db.query(Activity)

        if search is not None:
           all_activity_query = all_activity_query.filter(Activity.title.ilike(f"%{search}%"))

        all_activity = all_activity_query.order_by(Activity.id.desc()).all()

        return {
            'status': 'true',
            'message': 'User data retrieved successfully',
            'data': all_activity
        }
    except jwt.InvalidTokenError:
        return {"status": "false", "message": "Invalid token"}
    except Exception as e:
        return {"status": "false", "message": f"An error occurred: {str(e)}"}    


def delete_activity_by_token(activity_id: str, db: Session, admin_token: str):
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
        
        activity_details = db.query(Activity).filter(
            Activity.id == activity_id).first()
        
        if not activity_details:
            return {"status": 'false', 'message': "Activiy not found"}

        db.delete(activity_details)
        db.commit()

        response = {
            'status': 'true',
            'message': "Activity Details deleted successfully"
        }

        return response

    except jwt.InvalidTokenError:
        return {"status": "false", "message": "Invalid token"}
    except Exception as e:
        return {"status": "false", "message": f"An error occurred: {str(e)}"}
