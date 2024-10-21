from .models import ActivityDetails, ActivityDetailsCreate
from typing import List, Optional
from sqlmodel import Session
from datetime import datetime, timedelta
from fastapi import status, HTTPException
from src.parameter import  jwt, SECRET_KEY, ALGORITHM
from src.UserProfile.models import UserProfile
from src.Activity.models import Activity
from src.Chapter.models import Chapter
from src.Stories.models import Stories
from src.Character.models import Character
from src.ChapterWiseUser.models import ChapterWiseUser
from src.UserCharacter.models import Usercharacter


def get_all_activity_details(db: Session, admin_token: str, search:Optional[str] = None):
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

        all_activity_details_query = db.query(ActivityDetails)

        if search is not None:
           all_activity_details_query = all_activity_details_query.filter(ActivityDetails.title.ilike(f"%{search}%"))

        all_activity_details = all_activity_details_query.order_by(ActivityDetails.id.desc()).all()
        
        response = {
            'status': 'true',
            'message': "Data Received Successfully",
            'data': all_activity_details
        }
        return response

    except jwt.InvalidTokenError:
        return {"status": "false", "message": "Invalid token"}
    except Exception as e:
        return {"status": "false", "message": f"An error occurred: {str(e)}"}


def create(activity_details_create: ActivityDetailsCreate, db: Session, admin_token:str):
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
        
        activity_id = activity_details_create.activity_id
        
        existing_chapters = db.query(ActivityDetails).filter(ActivityDetails.activity_id == activity_id).all()
        
        # Determine the next chapter number
        next_sr_no = len(existing_chapters) + 1

        activity_details_create.sr_no = next_sr_no
        db_activity_details = ActivityDetails(**activity_details_create.dict())
        db.add(db_activity_details)
        db.commit()
        db.refresh(db_activity_details)
        response = {'status': 'true',
                'message': 'Activity Details Added Successfully', 'data': db_activity_details}

        return response

    except jwt.InvalidTokenError:
        return {"status": "false", "message": "Invalid token"}
    except Exception as e:
        return {"status": "false", "message": f"An error occurred: {str(e)}"}


def update(activity_details_id: str, activity_details_update: ActivityDetails, db: Session, admin_token: str):
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
        db_activity_details_update = activity_details_update.dict(exclude_unset=True)
        # Update user profile in the database
        db.query(ActivityDetails).filter(ActivityDetails.id ==
                                 activity_details_id).update(db_activity_details_update)
        db.commit()

        response = {
            'status': 'true',
            'message': "Activity Updated Successfully",
            'data': db_activity_details_update
        }
        return response

    except jwt.InvalidTokenError:
        return {"status": "false", "message": "Invalid token"}
    except Exception as e:
        return {"status": "false", "message": f"An error occurred: {str(e)}"}


def get_activity_deatils_by_token(activity_id: str, db: Session, user_token: str):
    try:
        # Decode the JWT token
        payload = jwt.decode(user_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")

        user_data = db.query(UserProfile).filter(UserProfile.id == user_id).first()

        if not user_data:
            return {"status": 'false', 'message': "User not found"}

        # Retrieve activity data along with chapter and story information
        activity_data = db.query(
            Activity,
            Chapter.name.label('chapter_name'),
            Chapter.chapter_no.label('chapter_no'),
            Stories.name.label('story_name')
        ).join(Chapter, Activity.chapter_id == Chapter.id).join(Stories, Activity.story_id == Stories.id).filter(Activity.id == activity_id).first()

        if not activity_data:
            return {"status": 'false', 'message': "Activity not found"}
        
        character = db.query(Character).filter(Character.stories_id == activity_data.Activity.story_id).first()
        
        if character:
            character_name = character.name
        else :
            character_name = None    

        # Retrieve activity details data
        activity_details_data = db.query(ActivityDetails).filter(ActivityDetails.activity_id == activity_id).all()

        if not activity_details_data:
            return {"status": 'false', 'message': "Activity details not found"}

        # Format activity details data
        details_list = []
        for detail in activity_details_data:
            details_list.append({
                'id': detail.id,
                'activity_id': detail.activity_id,
                'sr_no': detail.sr_no,
                'question': detail.question,
                'options': [detail.option_a, detail.option_b, detail.option_c, detail.option_d],
                'explation': detail.explation,
                'image': detail.image,
                'correct_answer': detail.correct_answer,
                'created_at': detail.created_at,
                'updated_at': detail.updated_at
            })

        return {
            'status': 'true',
            'message': 'Activity data retrieved successfully',
            'data': {
                'id': activity_data.Activity.id,
                'story_id': activity_data.Activity.story_id,
                'story_name': activity_data.story_name,
                'chapter_id': activity_data.Activity.chapter_id,
                'chapter_name': activity_data.chapter_name,
                'chapter_no': activity_data.chapter_no,
                'title': activity_data.Activity.title,
                'time': activity_data.Activity.time,
                'short_discription': activity_data.Activity.short_description,
                'activity_image': activity_data.Activity.activity_image,
                'image': activity_data.Activity.image,
                'audio': activity_data.Activity.audio,
                'document_english': activity_data.Activity.document_english,
                'document_japanese': activity_data.Activity.document_japanese,
                'character_name': character_name,
                'end_image': activity_data.Activity.end_image,
                'created_at': activity_data.Activity.created_at,
                'updated_at': activity_data.Activity.updated_at,
                'details': details_list
            }
        }
    except jwt.InvalidTokenError:
        return {"status": "false", "message": "Invalid token"}
    except Exception as e:
        return {"status": "false", "message": f"An error occurred: {str(e)}"}

def get_activities_and_details_by_chapter_id(chapter_id: str, db: Session, user_token: str):
    try:
        # Decode the JWT token
        payload = jwt.decode(user_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")

        user_data = db.query(UserProfile).filter(UserProfile.id == user_id).first()

        if not user_data:
            return {"status": 'false', 'message': "User not found"}

        # Retrieve activities data along with chapter and story information based on chapter_id
        activities_data = db.query(
            Activity,
            Chapter.name.label('chapter_name'),
            Chapter.chapter_no.label('chapter_no'),
            Stories.name.label('story_name')
        ).join(Chapter, Activity.chapter_id == Chapter.id).join(Stories, Activity.story_id == Stories.id).filter(Activity.chapter_id == chapter_id).all()
        

        if not activities_data:
            return {"status": 'false', 'message': "No activities found for the given chapter ID"}

        # Format activities data and include activity details
        activities_list = []
        for activity_data in activities_data:
            activity_details_data = db.query(ActivityDetails).filter(ActivityDetails.activity_id == activity_data.Activity.id).all()

            # Format activity details data
            details_list = []
            for detail in activity_details_data:
                details_list.append({
                    'id': detail.id,
                    'activity_id': detail.activity_id,
                    'sr_no': detail.sr_no,
                    'question': detail.question,
                    'options': [detail.option_a, detail.option_b, detail.option_c, detail.option_d],
                    'explation': detail.explation,
                    'image': detail.image,
                    'correct_answer': detail.correct_answer,
                    'created_at': detail.created_at,
                    'updated_at': detail.updated_at
                })
                
            charcter = db.query(Character).filter(Character.stories_id == activity_data.Activity.story_id).first()
            
            total_chapter = db.query(Chapter).filter(Chapter.stories_id == activity_data.Activity.story_id).count()
            
            if total_chapter :
                total_chapter = total_chapter
            else:
                total_chapter = None    
            
            
            # Handle the case where no character is found
            if charcter is not None:
                read_chapter = db.query(ChapterWiseUser).filter(ChapterWiseUser.user_id == user_id, ChapterWiseUser.stories_id == activity_data.Activity.story_id, ChapterWiseUser.read_status == "1").count()

                if read_chapter >= 3:
                    read_status = "yes"
                else:
                    read_status = "no"

                unlocked_character = db.query(Usercharacter).filter(Usercharacter.user_id == user_id, Usercharacter.character_id == charcter.id).first()

                if not unlocked_character:
                    unlocked_character_status = "no"
                else:
                    unlocked_character_status = "yes"

                character_name = charcter.name
                character_image = charcter.character_image
                character_id = charcter.id
            else:
                read_status = "no"
                unlocked_character_status = "no"
                character_name = None
                character_image = None
                character_id = None
     

            activities_list.append({
                'id': activity_data.Activity.id,
                'story_id': activity_data.Activity.story_id,
                'story_name': activity_data.story_name,
                'chapter_id': activity_data.Activity.chapter_id,
                'chapter_name': activity_data.chapter_name,
                'chapter_no': activity_data.chapter_no,
                'title': activity_data.Activity.title,
                'time': activity_data.Activity.time,
                'short_discription': activity_data.Activity.short_description,
                'activity_image': activity_data.Activity.activity_image,
                'document_english': activity_data.Activity.document_english,
                'document_japanese': activity_data.Activity.document_japanese,
                'character_name': character_name,
                'character_image': character_image,
                'character_id': character_id,
                'unlocked_character_status': unlocked_character_status,
                'read_status': read_status,
                'read_chapter_count': read_chapter if read_chapter else None,
                'total_chapter_count': total_chapter,
                'image': activity_data.Activity.image,
                'audio': activity_data.Activity.audio,
                'end_image': activity_data.Activity.end_image,
                'created_at': activity_data.Activity.created_at,
                'updated_at': activity_data.Activity.updated_at,
                'details': details_list
            })

        return {
            'status': 'true',
            'message': 'Activities data retrieved successfully',
            'data': activities_list
        }
    except jwt.InvalidTokenError:
        return {"status": "false", "message": "Invalid token"}
    except Exception as e:
        return {"status": "false", "message": f"An error occurred: {str(e)}"}
    
    
def get_all_activity_details_by_user_token(db: Session, user_token: str, search:Optional[str] = None):
    try:
        # Decode the JWT token
        payload = jwt.decode(user_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")

        user_data = db.query(UserProfile).filter(
            UserProfile.id == user_id).first()

        if not user_data:
            return {"status": 'false', 'message': "User not found"}
        
        all_activity_query = db.query(ActivityDetails)

        if search is not None:
           all_activity_query = all_activity_query.filter(ActivityDetails.title.ilike(f"%{search}%"))

        all_activity = all_activity_query.order_by(ActivityDetails.id.desc()).all()

        return {
            'status': 'true',
            'message': 'User data retrieved successfully',
            'data': all_activity
        }
    except jwt.InvalidTokenError:
        return {"status": "false", "message": "Invalid token"}
    except Exception as e:
        return {"status": "false", "message": f"An error occurred: {str(e)}"}   


def delete_activity_details_by_token(activity_details_id: str, db: Session, admin_token: str):
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
        
        activity_details = db.query(ActivityDetails).filter(
            ActivityDetails.id == activity_details_id).first()
        
        if not activity_details:
            return {"status": 'false', 'message': "Activiy Details not found"}

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
