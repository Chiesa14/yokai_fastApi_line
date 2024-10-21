from .models import CharacterChat,CharacterChatCreate,Batch
from typing import List, Optional
from sqlmodel import Session
from datetime import datetime, timedelta
from fastapi import status, HTTPException
from src.parameter import jwt, SECRET_KEY, ALGORITHM
from src.UserProfile.models import UserProfile
from sqlalchemy import func, and_
from src.Character.models import Character
from src.CharacterSummary.models import UserSummary

def create(db: Session, character_chat_create: CharacterChatCreate, user_token: str):
    try:
        # Decode the JWT token
        payload = jwt.decode(user_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")

        # Retrieve user data from the database using the user_id
        user_data = db.query(UserProfile).filter(UserProfile.id == user_id).first()

        if not user_data:
            return {"status": 'false', 'message': "User not found"}
        
        character_chat_create.user_id = user_id
        db_character_chat = CharacterChat(**character_chat_create.dict())
        db.add(db_character_chat)
        db.commit()
        db.refresh(db_character_chat)
        response = {'status': 'true', 'message': 'Character Chat Added Successfully', 'data': db_character_chat}

        return response

    except jwt.InvalidTokenError:
        return {"status": "false", "message": "Invalid token"}
    except Exception as e:
        return {"status": "false", "message": f"An error occurred: {str(e)}"}
    
def get_character_chat_by_user(user_token: str, character_id : str, db: Session, page_number: Optional[str] = None):
    try:
        # Decode the JWT token
        payload = jwt.decode(user_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")

        # Retrieve user data from the database using the user_id
        user_data = db.query(UserProfile).filter(
            UserProfile.id == user_id).first()

        if not user_data:
            return {"status": 'false', 'message': "User not found"}

        # Retrieve all user data if the user is an admin
        character_chat_query = db.query(CharacterChat).filter(
            CharacterChat.user_id == user_id, CharacterChat.character_id == character_id)
            
        try:
            page_number = int(page_number)
        except ValueError:
            page_number = 1  # Default to page 1 if conversion fails
        
        page_size = 10
        offset = (page_number - 1) * page_size
        
        total_data = character_chat_query.count()

        total_pages = (total_data + page_size - 1) // page_size  

        # Order the results by transaction ID in descending order and apply pagination
        character_chat = character_chat_query.order_by(CharacterChat.id.desc()).offset(offset).limit(page_size).all()
        
        character = db.query(Character).filter(Character.id == character_id).first()
        
        tags_array = character.tags.split(',') if character.tags else []
        
        summary_data = db.query(UserSummary).filter(UserSummary.user_id == user_id, UserSummary.character_id == character_id).first()
        
        if summary_data:
            summary = summary_data.summary
        else :
            summary = None    

        response = {
            'status': 'true',
            'message': "Data Received Successfully",
            'data': character_chat,
            'prompt': character.prompt,
            'tags': tags_array,
            'summary': summary,
            'character_id': character_id,
            'total_data': total_data,
            'total_pages': total_pages,
            'current_page': page_number,
            'page_size': page_size
        }
        return response

    except jwt.InvalidTokenError:
        return {"status": "false", "message": "Invalid token"}
    except Exception as e:
        return {"status": "false", "message": f"An error occurred: {str(e)}"}

# def get_character_chat_by_user(user_token: str, character_id: str, db: Session, page_number: Optional[str] = None):
#     try:
#         # Decrypt the token
#         decrypted_token = decrypt_token(user_token.encode(), fernet_key)

#         # Decode the JWT token without checking expiration
#         payload = jwt.decode(decrypted_token, jwt_secret_key, algorithms=["HS256"], options={"verify_exp": False})

#         # Extract user_id from the payload
#         user_id = payload.get('user_id')

#         # Retrieve user data from the database using the user_id
#         user_data = db.query(UserProfile).filter(UserProfile.id == user_id).first()

#         if not user_data:
#             return {"status": 'false', 'message': "User not found"}

#         # Check if the token is expired based on the database expiration date
#         current_time = datetime.now()
#         token_expiry_date = datetime.strptime(user_data.expire_session_token, '%Y-%m-%d %H:%M:%S.%f')
#         if token_expiry_date < current_time:
#             return {"status": "false", "message": "Token has expired"}

#         # Retrieve or create a batch entry for the user
#         batch_entry = db.query(Batch).filter(Batch.user_id == user_id).first()

#         if batch_entry:
#             # Parse last_hit_time as datetime object if it's not already
#             if isinstance(batch_entry.last_hit_time, str):
#                 last_hit_time = datetime.strptime(batch_entry.last_hit_time, '%Y-%m-%d %H:%M:%S.%f')
#             else:
#                 last_hit_time = batch_entry.last_hit_time

#             if last_hit_time.date() < current_time.date():
#                 # It's a new day
#                 if (current_time.date() - last_hit_time.date()).days > 1:
#                     # If the API wasn't called on the consecutive day, reset count to 1
#                     batch_entry.count = 1
#                 else:
#                     # Increment the count if the API is called on a consecutive day
#                     batch_entry.count += 1

#                 if batch_entry.count >= 30:
#                     batch_entry.count = 1  # Reset count to 1 when a new level is reached
#                     batch_entry.level += 1  # Increment level

#             # Check if the level has reached 30
#             if batch_entry.level >= 30:
#                 batch_entry.level += 1  # Increment level beyond 30 as required
#                 batch_entry.count = 1  # Reset count to 1

#             batch_entry.last_hit_time = current_time.strftime('%Y-%m-%d %H:%M:%S.%f')
#         else:
#             # No entry exists, create a new one
#             batch_entry = Batch(user_id=user_id, count=1, level=0, last_hit_time=current_time.strftime('%Y-%m-%d %H:%M:%S.%f'))
#             db.add(batch_entry)

#         db.commit()

#         # Retrieve character chat data
#         character_chat_query = db.query(CharacterChat).filter(CharacterChat.user_id == user_id, CharacterChat.character_id == character_id)

#         try:
#             page_number = int(page_number)
#         except ValueError:
#             page_number = 1  # Default to page 1 if conversion fails
        
#         page_size = 10
#         offset = (page_number - 1) * page_size
        
#         total_data = character_chat_query.count()
#         total_pages = (total_data + page_size - 1) // page_size  

#         # Order the results by transaction ID in descending order and apply pagination
#         character_chat = character_chat_query.order_by(CharacterChat.id.desc()).offset(offset).limit(page_size).all()
        
#         character = db.query(Character).filter(Character.id == character_id).first()
        
#         tags_array = character.tags.split(',') if character.tags else []

#         response = {
#             'status': 'true',
#             'message': "Data Received Successfully",
#             'data': character_chat,
#             'prompt': character.prompt,
#             'tags': tags_array,
#             'total_data': total_data,
#             'total_pages': total_pages,
#             'current_page': page_number,
#             'page_size': page_size
#         }
#         return response

#     except jwt.InvalidTokenError:
#         return {"status": "false", "message": "Invalid token"}
#     except Exception as e:
#         return {"status": "false", "message": f"An error occurred: {str(e)}"}
