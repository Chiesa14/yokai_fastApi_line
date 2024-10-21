from .models import ChapterWiseUser, ChapterWiseUserCreate, UpdateReadStatus
from typing import List, Optional
from sqlmodel import Session
from datetime import datetime, timedelta
from fastapi import status, HTTPException
from src.parameter import jwt, SECRET_KEY, ALGORITHM
from src.UserProfile.models import UserProfile
from src.Stories.models import Stories
from src.Chapter.models import Chapter
from src.Activity.models import Activity
from src.CharacterChat.models import Batch
from sqlalchemy import func, and_
import pytz


def get_chapters_by_stories_id_for_user(stories_id: Optional[str], db: Session, user_token: str, search: Optional[str] = None):
    try:
        # Decode the JWT token
        payload = jwt.decode(user_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")

        # Retrieve user data from the database using the user_id
        user_data = db.query(UserProfile).filter(
            UserProfile.id == user_id).first()

        if not user_data:
            return {"status": 'false', 'message': "User not found"}

        # Initialize response data
        response_data = {}

        # Query to get chapters for the specific user and stories_id
        chapter_query = db.query(ChapterWiseUser).filter(
            ChapterWiseUser.user_id == user_id
        )

        if stories_id:
            chapter_query = chapter_query.filter(
                ChapterWiseUser.stories_id == stories_id)

        if search:
            chapter_query = chapter_query.join(Chapter, Chapter.id == ChapterWiseUser.chapter_id).filter(
                Chapter.name.ilike(f"%{search}%")
            )

        # Fetch chapter data
        chapter_data_list = chapter_query.all()

        # Prepare response data
        chapter_details_list = []
        story_info = None
        for chapter_data in chapter_data_list:
            chapter_info = db.query(Chapter).filter(
                Chapter.id == chapter_data.chapter_id).first()

            if chapter_info:
                # Check if there is an activity for this chapter
                activity_exists = db.query(Activity).filter(
                    Activity.chapter_id == chapter_info.id).first()

                # Determine activity_status
                activity_status = "yes" if activity_exists else "no"

                # Fetch the story details only once
                if not story_info:
                    story_info = db.query(Stories).filter(
                        Stories.id == chapter_info.stories_id).first()

                # Create a dictionary with chapter details and activity_status
                chapter_dict = {
                    'id': chapter_info.id,
                    'stories_id': chapter_info.stories_id,
                    'name': chapter_info.name,
                    'chapter_no': chapter_info.chapter_no,
                    'chapter_document_english': chapter_info.chapter_document_english,
                    'chapter_document_japanese': chapter_info.chapter_document_japanese,
                    'created_at': chapter_info.created_at,
                    'updated_at': chapter_info.updated_at,
                    'activity_status': activity_status,
                    'read_status': chapter_data.read_status
                }

                chapter_details_list.append(chapter_dict)

        if story_info:
            response_data = {
                'id': story_info.id,
                'name': story_info.name,
                'description': story_info.discription,
                'stories_image': story_info.stories_image,
                'created_at': story_info.created_at,
                'updated_at': story_info.updated_at,
                'chapter_data': chapter_details_list
            }

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
    
# def get_latest_chapters_by_user(db: Session, user_token: str):
#     try:
#         # Decode the JWT token
#         payload = jwt.decode(user_token, SECRET_KEY, algorithms=[ALGORITHM])
#         user_id = payload.get("user_id")

#         # Retrieve user data from the database using the user_id
#         user_data = db.query(UserProfile).filter(
#             UserProfile.id == user_id).first()

#         if not user_data:
#             return {"status": 'false', 'message': "User not found"}

#         # Query to get the latest chapters for the specific user, excluding null read_date
#         chapter_query = db.query(ChapterWiseUser).filter(
#             ChapterWiseUser.user_id == user_id,
#             ChapterWiseUser.read_date.isnot(None)
#         ).order_by(ChapterWiseUser.read_date.desc()).limit(5)

#         # Fetch chapter data
#         chapter_data_list = chapter_query.all()

#         if not chapter_data_list:
#             return {"status": "false", "message": "No chapters found"}

#         # Prepare response data
#         chapter_details_list = []
#         story_info = None
#         for chapter_data in chapter_data_list:
#             chapter_info = db.query(Chapter).filter(
#                 Chapter.id == chapter_data.chapter_id).first()

#             if chapter_info:
#                 # Check if there is an activity for this chapter
#                 activity_exists = db.query(Activity).filter(
#                     Activity.chapter_id == chapter_info.id).first()

#                 # Determine activity_status
#                 activity_status = "yes" if activity_exists else "no"

#                 story_info = db.query(Stories).filter(Stories.id == chapter_info.stories_id).first()
                    
#                 story_name = story_info.name
#                 story_image = story_info.stories_image    

#                 # Create a dictionary with chapter details and activity_status
#                 chapter_dict = {
#                     'id': chapter_info.id,
#                     'stories_id': chapter_info.stories_id,
#                     'name': chapter_info.name,
#                     'chapter_no': chapter_info.chapter_no,
#                     'chapter_document_english': chapter_info.chapter_document_english,
#                     'chapter_document_japanese': chapter_info.chapter_document_japanese,
#                     'created_at': chapter_info.created_at,
#                     'updated_at': chapter_info.updated_at,
#                     'story_name': story_name,
#                     'story_image': story_image,
#                     'activity_status': activity_status,
#                     'read_status': chapter_data.read_status,
#                     'read_date': chapter_data.read_date
#                 }

#                 chapter_details_list.append(chapter_dict)

#         response = {
#             'status': 'true',
#             'message': "Data Received Successfully",
#             'data': chapter_details_list
#         }

#         return response

#     except jwt.InvalidTokenError:
#         return {"status": "false", "message": "Invalid token"}
#     except Exception as e:
#         return {"status": "false", "message": f"An error occurred: {str(e)}"}

def get_latest_chapters_by_user(db: Session, user_token: str):
    try:
        # Decode the JWT token
        payload = jwt.decode(user_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")

        # Retrieve user data from the database using the user_id
        user_data = db.query(UserProfile).filter(UserProfile.id == user_id).first()

        if not user_data:
            return {"status": 'false', 'message': "User not found"}

        # Subquery to find the latest chapter read date for each story
        subquery = (
            db.query(
                ChapterWiseUser.stories_id,
                func.max(ChapterWiseUser.read_date).label("latest_read_date")
            )
            .filter(
                ChapterWiseUser.user_id == user_id,
                ChapterWiseUser.read_date.isnot(None)
            )
            .group_by(ChapterWiseUser.stories_id)
            .subquery()
        )

        # Main query to get the latest chapter details for each story
        latest_chapters_query = (
            db.query(ChapterWiseUser)
            .join(subquery, and_(
                ChapterWiseUser.stories_id == subquery.c.stories_id,
                ChapterWiseUser.read_date == subquery.c.latest_read_date
            ))
            .order_by(ChapterWiseUser.read_date.desc())
        )

        # Fetch chapter data
        chapter_data_list = latest_chapters_query.all()

        if not chapter_data_list:
            return {"status": "false", "message": "No chapters found"}

        # Prepare response data
        chapter_details_list = []
        for chapter_data in chapter_data_list:
            chapter_info = db.query(Chapter).filter(
                Chapter.id == chapter_data.chapter_id).first()

            if chapter_info:
                # Check if there is an activity for this chapter
                activity_exists = db.query(Activity).filter(
                    Activity.chapter_id == chapter_info.id).first()

                # Determine activity_status
                activity_status = "yes" if activity_exists else "no"

                story_info = db.query(Stories).filter(
                    Stories.id == chapter_info.stories_id).first()

                story_name = story_info.name if story_info else None
                story_image = story_info.stories_image if story_info else None

                # Create a dictionary with chapter details and activity_status
                chapter_dict = {
                    'id': chapter_info.id,
                    'stories_id': chapter_info.stories_id,
                    'name': chapter_info.name,
                    'chapter_no': chapter_info.chapter_no,
                    'chapter_document_english': chapter_info.chapter_document_english,
                    'chapter_document_japanese': chapter_info.chapter_document_japanese,
                    'created_at': chapter_info.created_at,
                    'updated_at': chapter_info.updated_at,
                    'story_name': story_name,
                    'story_image': story_image,
                    'activity_status': activity_status,
                    'read_status': chapter_data.read_status,
                    'read_date': chapter_data.read_date
                }

                chapter_details_list.append(chapter_dict)

        response = {
            'status': 'true',
            'message': "Data Received Successfully",
            'data': chapter_details_list
        }

        return response

    except jwt.InvalidTokenError:
        return {"status": "false", "message": "Invalid token"}
    except Exception as e:
        return {"status": "false", "message": f"An error occurred: {str(e)}"}

# def update_read_status(user_token: str, chapter_id: str, read_data: UpdateReadStatus, db: Session):
#     try:
#         # Decode the JWT token
#         payload = jwt.decode(user_token, SECRET_KEY, algorithms=[ALGORITHM])
#         user_id = payload.get("user_id")

#         # Retrieve user data from the database using the user_id
#         user_profile = db.query(UserProfile).filter(
#             UserProfile.id == user_id).first()

#         if not user_profile:
#             return {"status": 'false', 'message': "User not found"}

#         chapter_user_data = db.query(ChapterWiseUser).filter(
#             ChapterWiseUser.user_id == user_id, ChapterWiseUser.chapter_id == chapter_id).first()

#         if not chapter_user_data:
#             return {"status": 'false', 'message': "User Chapter not found"}
        
#         india_tz = pytz.timezone('Asia/Kolkata')
    
#          # Get the current time in the specified timezone
#         now = datetime.now(india_tz)

#         # Update read status and updated_at timestamp
#         chapter_user_data.read_status = read_data.read_status
#         chapter_user_data.read_date = now 
#         db.commit()

#         return {
#             'status': 'true',
#             'message': "User Chapter Updated Successfully"
#         }

#     except jwt.InvalidTokenError:
#         return {"status": "false", "message": "Invalid token"}
#     except Exception as e:
#         return {"status": "false", "message": f"An error occurred: {str(e)}"}

def update_read_status(user_token: str, chapter_id: str, read_data: UpdateReadStatus, db: Session):
    try:
        # Decode the JWT token
        payload = jwt.decode(user_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")

        # Retrieve user data from the database using the user_id
        user_profile = db.query(UserProfile).filter(
            UserProfile.id == user_id).first()

        if not user_profile:
            return {"status": 'false', 'message': "User not found"}

        chapter_user_data = db.query(ChapterWiseUser).filter(
            ChapterWiseUser.user_id == user_id, ChapterWiseUser.chapter_id == chapter_id).first()

        if not chapter_user_data:
            return {"status": 'false', 'message': "User Chapter not found"}
        
        india_tz = pytz.timezone('Asia/Kolkata')
    
        # Get the current time in the specified timezone
        now = datetime.now(india_tz)

        # Update read status and updated_at timestamp
        chapter_user_data.read_status = read_data.read_status
        chapter_user_data.read_date = now 
        db.commit()

        if read_data.read_status == "1":
            start_of_week = now - timedelta(days=now.weekday())

            # Count how many chapters the user has read this week
            chapters_read_this_week = db.query(ChapterWiseUser).filter(
                ChapterWiseUser.user_id == user_id,
                ChapterWiseUser.read_status == "1",
                ChapterWiseUser.read_date >= start_of_week
            ).count()

            if chapters_read_this_week >= 5:
                batch_entry = db.query(Batch).filter(Batch.user_id == user_id).first()

                if batch_entry:
                    if batch_entry.batch == "0":
                        batch_entry.batch = "1"
                        db.commit()
                else:
                    new_batch_entry = Batch(user_id=user_id, level=None, count=None, last_hit_time=None, batch="1")
                    db.add(new_batch_entry)
                    db.commit()

        return {
            'status': 'true',
            'message': "User Chapter Updated Successfully"
        }

    except jwt.InvalidTokenError:
        return {"status": "false", "message": "Invalid token"}
    except Exception as e:
        return {"status": "false", "message": f"An error occurred: {str(e)}"}


def add_chapters_for_all_users(db: Session):
    try:
        # Retrieve all users from the user_profile table
        users = db.query(UserProfile).all()

        if not users:
            return {"status": 'false', 'message': "No users found"}

        # Retrieve all chapters from the chapter table
        chapters = db.query(Chapter).all()

        if not chapters:
            return {"status": 'false', 'message': "No chapters found"}

        # List to hold all ChapterWiseUser entries
        chapter_wise_user_entries = []

        for user in users:
            for chapter in chapters:
                # Create a new ChapterWiseUser entry for each user and chapter
                new_entry = ChapterWiseUser(
                    user_id=user.id,
                    chapter_id=chapter.id,
                    stories_id=chapter.stories_id,
                    read_status="0"
                )
                chapter_wise_user_entries.append(new_entry)

        # Add all entries to the session and commit
        db.add_all(chapter_wise_user_entries)
        db.commit()

        return {"status": 'true', 'message': "Chapters added for all users successfully"}

    except Exception as e:
        db.rollback()
        return {"status": "false", "message": f"An error occurred: {str(e)}"}
