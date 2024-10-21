from .models import Chapter,ChapterCreate
from typing import List, Optional
from sqlmodel import Session
from datetime import datetime, timedelta
from fastapi import status, HTTPException
from src.parameter import  jwt, SECRET_KEY, ALGORITHM
from src.UserProfile.models import UserProfile
from src.Stories.models import Stories
from src.Activity.models import Activity
from src.ChapterWiseUser.models import ChapterWiseUser
import pytz

# def get_chapter_by_storie_id(stories_id:str, db: Session, user_token: str, search: Optional[str] = None):
#     try:
#         # Decrypt the token
#         decrypted_token = decrypt_token(user_token.encode(), fernet_key)

#         # Decode the JWT token
#         payload = jwt.decode(decrypted_token, jwt_secret_key, algorithms=["HS256"])

#         # Extract user_id from the payload
#         user_id = payload.get('user_id')

#         # Retrieve user data from the database using the user_id
#         user_data = db.query(UserProfile).filter(UserProfile.id == user_id).first()

#         if not user_data:
#             return {"status": 'false', 'message': "User not found"}
        
#         # Retrieve stories data
#         stories_data = db.query(Stories).filter(Stories.id == stories_id).first()
        
#         if not stories_data:
#             return {"status": 'false', 'message': "Stories not found"}

#         # Query chapters related to the story
#         chapter_query = db.query(Chapter).filter(Chapter.stories_id == stories_id)

#         if search:
#             chapter_query = chapter_query.filter(Chapter.name.ilike(f"%{search}%"))

#         # Fetch all chapters ordered by id descending
#         chapter_details = chapter_query.order_by(Chapter.id.desc()).all()
        
#         details_array = []
        
#         for chapter_data in chapter_details:
#             # Check if there is an activity for this chapter
#             activity_exists = db.query(Activity).filter(Activity.chapter_id == chapter_data.id).first()
            
#             # Determine activity_status
#             activity_status = "yes" if activity_exists else "no"
            
#             # Create a dictionary with chapter details and activity_status
#             chapter_dict = {
#                 'id': chapter_data.id,
#                 'stories_id': chapter_data.stories_id,
#                 'name': chapter_data.name,
#                 'chapter_no': chapter_data.chapter_no,
#                 'chapter_document_english': chapter_data.chapter_document_english,
#                 'chapter_document_japanese': chapter_data.chapter_document_japanese,
#                 'created_at': chapter_data.created_at,
#                 'updated_at': chapter_data.updated_at,
#                 'activity_status': activity_status
#             }
            
#             details_array.append(chapter_dict)
        
#         # Include details_array in the stories_data or data response
#         stories_data = {
#             'id': stories_data.id,
#             'name': stories_data.name,
#             'discription': stories_data.discription,
#               'stories_image': stories_data.stories_image,
#               'created_at': stories_data.created_at,
#               'updated_at': stories_data.updated_at,
#             'chapter_data': details_array  # Include chapters array inside stories_data
#         }
        
#         response = {
#             'status': 'true',
#             'message': "Data Received Successfully",
#             'data': stories_data  # Return stories_data instead of details_array directly
#         }
        
#         return response

#     except jwt.ExpiredSignatureError:
#         return {"status": "false", "message": "Token has expired"}
#     except jwt.InvalidTokenError:
#         return {"status": "false", "message": "Invalid token"}
#     except InvalidToken:
#         return {"status": "false", "message": "Invalid or corrupted token"}

def get_chapter_by_storie_id(stories_id: Optional[str], db: Session, user_token: str, search: Optional[str] = None):
    try:
        # Decode the JWT token
        payload = jwt.decode(user_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")

        # Retrieve user data from the database using the user_id
        user_data = db.query(UserProfile).filter(UserProfile.id == user_id).first()

        if not user_data:
            return {"status": 'false', 'message': "User not found"}

        if stories_id:
            # Retrieve specific story data
            stories_data = db.query(Stories).filter(Stories.id == stories_id).first()
            
            if not stories_data:
                return {"status": 'false', 'message': "Story not found"}

            # Query chapters related to the specific story
            chapter_query = db.query(Chapter).filter(Chapter.stories_id == stories_id)
        else:
            # Query all chapters
            chapter_query = db.query(Chapter)

        if search:
            chapter_query = chapter_query.filter(Chapter.name.ilike(f"%{search}%"))

        # Fetch all chapters ordered by id descending
        chapter_details = chapter_query.order_by(Chapter.id.desc()).all()
        
        details_array = []
        for chapter_data in chapter_details:
            # Check if there is an activity for this chapter
            activity_exists = db.query(Activity).filter(Activity.chapter_id == chapter_data.id).first()
            
            # Determine activity_status
            activity_status = "yes" if activity_exists else "no"
            
            # Create a dictionary with chapter details and activity_status
            chapter_dict = {
                'id': chapter_data.id,
                'stories_id': chapter_data.stories_id,
                'name': chapter_data.name,
                'chapter_no': chapter_data.chapter_no,
                'chapter_document_english': chapter_data.chapter_document_english,
                'chapter_document_japanese': chapter_data.chapter_document_japanese,
                'created_at': chapter_data.created_at,
                'updated_at': chapter_data.updated_at,
                'activity_status': activity_status
            }
            
            details_array.append(chapter_dict)

        if stories_id:
            # Include story details if a specific story ID is provided
            response_data = {
                'id': stories_data.id,
                'name': stories_data.name,
                'discription': stories_data.discription,
                'stories_image': stories_data.stories_image,
                'created_at': stories_data.created_at,
                'updated_at': stories_data.updated_at,
                'chapter_data': details_array  # Include chapters array inside stories_data
            }
        else:
            # Only include chapter details if no specific story ID is provided
            response_data = {
                'chapter_data': details_array
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


def create(chapter_create: ChapterCreate, db: Session, admin_token:str):
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
        
        stories_id = chapter_create.stories_id
        
        stories_data = db.query(Stories).filter(
            Stories.id == stories_id).first()
        
        if not stories_data:
            return {"status": 'false', 'message': "Stories not found"}
        
        # Get all chapters for the given stories_id to determine the next chapter number
        existing_chapters = db.query(Chapter).filter(Chapter.stories_id == stories_id).all()
        
        # Determine the next chapter number
        next_chapter_number = len(existing_chapters) + 1

        # Create the chapter title
        chapter_title = f"Chapter {next_chapter_number}"

        chapter_create.chapter_no = chapter_title
        db_chapter = Chapter(**chapter_create.dict())
        db.add(db_chapter)
        db.commit()
        db.refresh(db_chapter)
        
        users = db.query(UserProfile).all()
        
        for user in users:
         new_entry = ChapterWiseUser(
            user_id=user.id,
            chapter_id=db_chapter.id,
            stories_id=db_chapter.stories_id,
            read_status="0"
        )
         db.add(new_entry)
         db.commit()

        
        response = {'status': 'true',
                'message': 'Chapter Details Added Successfully', 'data': db_chapter}

        return response

    except jwt.InvalidTokenError:
        return {"status": "false", "message": "Invalid token"}
    except Exception as e:
        return {"status": "false", "message": f"An error occurred: {str(e)}"}


def update(chapter_id: str, chapter_update: Stories, db: Session, admin_token: str):
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
        db_chapter_update = chapter_update.dict(exclude_unset=True)
        india_tz = pytz.timezone('Asia/Kolkata')
    
        # Get the current time in the specified timezone
        now = datetime.now(india_tz)
        db_chapter_update['updated_at'] = now
        # Update user profile in the database
        db.query(Chapter).filter(Chapter.id ==
                                 chapter_id).update(db_chapter_update)
        db.commit()

        response = {
            'status': 'true',
            'message': "Chapter Details Updated Successfully",
            'data': db_chapter_update
        }
        return response

    except jwt.InvalidTokenError:
        return {"status": "false", "message": "Invalid token"}
    except Exception as e:
        return {"status": "false", "message": f"An error occurred: {str(e)}"}


def get_chapter_by_token(chapter_id: str, db: Session, user_token: str):
    try:
        # Decode the JWT token
        payload = jwt.decode(user_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")

        user_data = db.query(UserProfile).filter(
            UserProfile.id == user_id).first()

        if not user_data:
            return {"status": 'false', 'message': "User not found"}

        # Retrieve user data from the database using the user_id
        chapter_data = db.query(Chapter).filter(
            Chapter.id == chapter_id).first()
        
        if not chapter_data:
            return {"status": 'false', 'message': "Chapter not found"}
        
        story_data = db.query(Stories).filter(Stories.id == chapter_data.stories_id).first()
        story_name = story_data.name

        return {
            'status': 'true',
            'message': 'User data retrieved successfully',
            'data': {
                'stories_id': chapter_data.stories_id,
                'story_name' : story_name,
                'name': chapter_data.name,
                'chapter_no': chapter_data.chapter_no,
                'chapter_document_english': chapter_data.chapter_document_english,
                'chapter_document_japanese': chapter_data.chapter_document_japanese,
                'created_at': chapter_data.created_at,
                'updated_at': chapter_data.updated_at
            }
        }
    except jwt.InvalidTokenError:
        return {"status": "false", "message": "Invalid token"}
    except Exception as e:
        return {"status": "false", "message": f"An error occurred: {str(e)}"}


def delete_chapter_by_token(chapter_id: str, db: Session, admin_token: str):
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
        
        chapter_details = db.query(Chapter).filter(
            Chapter.id == chapter_id).first()
        
        if not chapter_details:
            return {"status": 'false', 'message': "Chapter not found"}
        
        db.query(ChapterWiseUser).filter(ChapterWiseUser.chapter_id == chapter_id).delete()

        db.delete(chapter_details)
        db.commit()

        response = {
            'status': 'true',
            'message': "Chapter Details deleted successfully"
        }

        return response

    except jwt.InvalidTokenError:
        return {"status": "false", "message": "Invalid token"}
    except Exception as e:
        return {"status": "false", "message": f"An error occurred: {str(e)}"}
