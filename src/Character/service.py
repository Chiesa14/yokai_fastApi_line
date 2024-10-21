from .models import Character, CharacterCreate
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
from src.ChapterWiseUser.models import ChapterWiseUser
from sqlalchemy import func
from src.Chapter.models import Chapter
from src.CharacterChat.models import CharacterChat


def get_all_character(db: Session, admin_token: str, search: Optional[str] = None):
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

        all_character_query = db.query(Character)

        if search is not None:
            all_character_query = all_character_query.filter(
                Character.name.ilike(f"%{search}%"))

        all_character = all_character_query.order_by(Character.id.desc()).all()

        # Process characters to include tags as arrays
        processed_characters = []
        for character in all_character:
            story_data = db.query(Stories).filter(
                Stories.id == character.stories_id).first()
            tags_array = character.tags.split(',') if character.tags else []
            processed_characters.append({
                'id': character.id,
                'name': character.name,
                'stories_id': character.stories_id,
                'link': character.link,
                'introducation': character.introduction,
                'prompt': character.prompt,
                'character_image': character.character_image,
                'requirements': character.requirements,
                'tags': tags_array,
                'story_name': story_data.name,
                'created_at': character.created_at,
                'updated_at': character.updated_at
            })

        response = {
            'status': 'true',
            'message': "Data Received Successfully",
            'data': processed_characters
        }
        return response

    except jwt.InvalidTokenError:
        return {"status": "false", "message": "Invalid token"}
    except Exception as e:
        return {"status": "false", "message": f"An error occurred: {str(e)}"}


def get_all_character_by_user(db: Session, user_token: str, search: Optional[str] = None):
    try:
        # Decode the JWT token
        payload = jwt.decode(user_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")

        # Retrieve user data from the database using the user_id
        user_data = db.query(UserProfile).filter(
            UserProfile.id == user_id).first()

        if not user_data:
            return {"status": 'false', 'message': "User not found"}

        all_character_query = db.query(Character)

        if search is not None:
            all_character_query = all_character_query.filter(
                Character.name.ilike(f"%{search}%"))

        all_character = all_character_query.order_by(Character.id.desc()).all()

        # Process characters to include tags as arrays
        processed_characters = []
        for character in all_character:
            story_data = db.query(Stories).filter(
                Stories.id == character.stories_id).first()
            tags_array = character.tags.split(',') if character.tags else []
            processed_characters.append({
                'id': character.id,
                'name': character.name,
                'stories_id': character.stories_id,
                'link': character.link,
                'introducation': character.introduction,
                'prompt': character.prompt,
                'character_image': character.character_image,
                'requirements': character.requirements,
                'tags': tags_array,
                'story_name': story_data.name,
                'created_at': character.created_at,
                'updated_at': character.updated_at
            })

        response = {
            'status': 'true',
            'message': "Data Received Successfully",
            'data': processed_characters
        }
        return response

    except jwt.InvalidTokenError:
        return {"status": "false", "message": "Invalid token"}
    except Exception as e:
        return {"status": "false", "message": f"An error occurred: {str(e)}"}


def get_character_by_id(db: Session, admin_token: str, character_id: int):
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

        # Retrieve character data by character_id
        character = db.query(Character).filter(
            Character.id == character_id).first()

        if not character:
            return {"status": 'false', 'message': "Character not found"}

        story_data = db.query(Stories).filter(
            Stories.id == character.stories_id).first()

        # Process tags to split them into an array
        tags_array = character.tags.split(',') if character.tags else []

        character_data = {
            'id': character.id,
            'name': character.name,
            'stories_id': character.stories_id,
            'link': character.link,
            'introducation': character.introduction,
            'character_image': character.character_image,
            'requirements': character.requirements,
            'prompt': character.prompt,
            'tags': tags_array,
            'story_name': story_data.name,
            'created_at': character.created_at,
            'updated_at': character.updated_at
        }

        response = {
            'status': 'true',
            'message': "Data Received Successfully",
            'data': character_data
        }
        return response

    except jwt.InvalidTokenError:
        return {"status": "false", "message": "Invalid token"}
    except Exception as e:
        return {"status": "false", "message": f"An error occurred: {str(e)}"}


def get_character_by_user(db: Session, user_token: str, character_id: int):
    try:
        # Decode the JWT token
        payload = jwt.decode(user_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")

        # Retrieve user data from the database using the user_id
        user_data = db.query(UserProfile).filter(
            UserProfile.id == user_id).first()

        if not user_data:
            return {"status": 'false', 'message': "User not found"}

        # Retrieve character data by character_id
        character = db.query(Character).filter(
            Character.id == character_id).first()

        if not character:
            return {"status": 'false', 'message': "Character not found"}

        story_data = db.query(Stories).filter(
            Stories.id == character.stories_id).first()

        total_chapter = db.query(Chapter).filter(
            Chapter.stories_id == character.stories_id).count()

        total_read_chapter = db.query(ChapterWiseUser).filter(ChapterWiseUser.user_id == user_id,
                                                              ChapterWiseUser.stories_id == character.stories_id, ChapterWiseUser.read_status == "1").count()

        # Process tags to split them into an array
        tags_array = character.tags.split(',') if character.tags else []

        character_data = {
            'id': character.id,
            'name': character.name,
            'stories_id': character.stories_id,
            'link': character.link,
            'introducation': character.introduction,
            'character_image': character.character_image,
            'requirements': character.requirements,
            'prompt': character.prompt,
            'tags': tags_array,
            'story_name': story_data.name,
            'total_chapter': total_chapter,
            'total_read_chapter': total_read_chapter,
            'created_at': character.created_at,
            'updated_at': character.updated_at
        }

        response = {
            'status': 'true',
            'message': "Data Received Successfully",
            'data': character_data
        }
        return response

    except jwt.InvalidTokenError:
        return {"status": "false", "message": "Invalid token"}
    except Exception as e:
        return {"status": "false", "message": f"An error occurred: {str(e)}"}


def create(character_create: CharacterCreate, db: Session, admin_token: str):
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

        name = character_create.name
        stories_id = character_create.stories_id

        existing_story = db.query(Character).filter(
            Character.stories_id == stories_id).all()
        if len(existing_story) > 0:
            return {'status': 'false', 'message': 'This Story Character is already added.'}

        existing_email_profiles = db.query(
            Character).filter(Character.name == name).all()
        if len(existing_email_profiles) > 0:
            return {'status': 'false', 'message': 'This Character Name Is already Saved.'}

        db_character = Character(**character_create.dict())
        db.add(db_character)
        db.commit()
        db.refresh(db_character)
        response = {'status': 'true',
                    'message': 'Character Added Successfully', 'data': db_character}

        return response

    except jwt.InvalidTokenError:
        return {"status": "false", "message": "Invalid token"}
    except Exception as e:
        return {"status": "false", "message": f"An error occurred: {str(e)}"}


def update(character_id: str, character_update: Character, db: Session, admin_token: str):
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

        # if character_update.name:
        #     existing_character = db.query(Character).filter(Character.name == character_update.name).first()
        #     if existing_character and existing_character.id != character_id:
        #         return {"status": 'false', 'message': "Character name already exists"}

        # Prepare the update data
        db_character_update = character_update.dict(
            exclude_unset=True)
        # Update user profile in the database
        db.query(Character).filter(Character.id ==
                                   character_id).update(db_character_update)
        db.commit()

        response = {
            'status': 'true',
            'message': "Character Updated Successfully",
            'data': db_character_update
        }
        return response

    except jwt.InvalidTokenError:
        return {"status": "false", "message": "Invalid token"}
    except Exception as e:
        return {"status": "false", "message": f"An error occurred: {str(e)}"}


def delete_character_by_token(character_id: str, db: Session, admin_token: str):
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

        activity_details = db.query(Character).filter(
            Character.id == character_id).first()

        if not activity_details:
            return {"status": 'false', 'message': "Character not found"}

        db.delete(activity_details)
        db.commit()

        response = {
            'status': 'true',
            'message': "Character Details deleted successfully"
        }

        return response

    except jwt.InvalidTokenError:
        return {"status": "false", "message": "Invalid token"}
    except Exception as e:
        return {"status": "false", "message": f"An error occurred: {str(e)}"}


def get_unlocked_characters_for_user(db: Session, user_token: str, search: Optional[str] = None):
    try:
        # Decode the JWT token
        payload = jwt.decode(user_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")

        # Retrieve user data from the database using the user_id
        user_data = db.query(UserProfile).filter(
            UserProfile.id == user_id).first()

        if not user_data:
            return {"status": 'false', 'message': "User not found"}

        stories = db.query(Stories).all()

        # Initialize an empty list to store valid stories_ids
        valid_stories_ids = []

        # Iterate over each story and count read_status entries for the given user_id
        for story in stories:
            read_status_count = db.query(ChapterWiseUser).filter(
                ChapterWiseUser.user_id == user_id,
                ChapterWiseUser.stories_id == story.id,
                ChapterWiseUser.read_status == "1"
            ).count()

            # Include stories_id in the valid_stories_ids list if read_status count is less than 5
            if read_status_count >= 3:
                valid_stories_ids.append(story.id)

        # Fetch all characters for the valid stories_ids
        if search:
            characters_data = db.query(Character).filter(
                Character.stories_id.in_(valid_stories_ids),
                Character.name.ilike(f'%{search}%')
            ).all()
        else:
            characters_data = db.query(Character).filter(
                Character.stories_id.in_(valid_stories_ids)
            ).all()

        # Prepare character details
        character_details = []
        for character in characters_data:
            character_chat = db.query(CharacterChat).filter(CharacterChat.user_id == user_id, CharacterChat.character_id == character.id).order_by(CharacterChat.id.desc()).first()    
            
            if character_chat:  
                if character_chat.question:
                    message = character_chat.question
                    last_message_time = character_chat.created_at
                else:
                    message = character_chat.answer
                    last_message_time = character_chat.created_at
            else:
                message = None
                last_message_time = None         
                   
            character_dict = {
                'id': character.id,
                'prompt': character.prompt,
                'name': character.name,
                'stories_id': character.stories_id,
                'link': character.link,
                'introducation': character.introduction,
                'character_image': character.character_image,
                'requirements': character.requirements,
                'latest_message': message,
                'last_message_time': last_message_time,
                'tags': character.tags,
                'created_at': character.created_at,
                'updated_at': character.updated_at,
            }
            character_details.append(character_dict)

        # Prepare the response
        response = {
            'status': 'true',
            'message': "Data Received Successfully",
            # 'story_data': valid_stories_ids,
            'data': character_details
        }

        return response

    except jwt.InvalidTokenError:
        return {"status": "false", "message": "Invalid token"}
    except Exception as e:
        return {"status": "false", "message": f"An error occurred: {str(e)}"}


def get_locked_characters_for_user(db: Session, user_token: str, search: Optional[str] = None):
    try:
        # Decode the JWT token
        payload = jwt.decode(user_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")

        # Retrieve user data from the database using the user_id
        user_data = db.query(UserProfile).filter(
            UserProfile.id == user_id).first()

        if not user_data:
            return {"status": 'false', 'message': "User not found"}

        stories = db.query(Stories).all()

        # Initialize an empty list to store valid stories_ids
        valid_stories_ids = []

        # Iterate over each story and count read_status entries for the given user_id
        for story in stories:
            read_status_count = db.query(ChapterWiseUser).filter(
                ChapterWiseUser.user_id == user_id,
                ChapterWiseUser.stories_id == story.id,
                ChapterWiseUser.read_status == "1"
            ).count()

            # Include stories_id in the valid_stories_ids list if read_status count is less than 5
            if read_status_count < 3:
                valid_stories_ids.append(story.id)

        # Fetch all characters for the valid stories_ids
        if search:
            characters_data = db.query(Character).filter(
                Character.stories_id.in_(valid_stories_ids),
                Character.name.ilike(f'%{search}%')
            ).all()
        else:
            characters_data = db.query(Character).filter(
                Character.stories_id.in_(valid_stories_ids),
            ).order_by(Character.id.desc()).all()

        # Prepare character details
        character_details = []
        for character in characters_data:
            character_dict = {
                'id': character.id,
                'prompt': character.prompt,
                'name': character.name,
                'stories_id': character.stories_id,
                'introducation': character.introduction,
                'character_image': character.character_image,
                'created_at': character.created_at,
                'updated_at': character.updated_at
            }
            character_details.append(character_dict)

        # Prepare the response
        response = {
            'status': 'true',
            'message': "Data Received Successfully",
            # 'story_data': valid_stories_ids,
            'data': character_details
        }

        return response

    except jwt.InvalidTokenError:
        return {"status": "false", "message": "Invalid token"}
    except Exception as e:
        return {"status": "false", "message": f"An error occurred: {str(e)}"}