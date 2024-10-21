from service_identity import cryptography
from .models import UserProfile, UserProfileCreate, UpdatePassword, UpdateAccountStatus
from typing import List, Optional
from sqlmodel import Session
from datetime import datetime, timedelta
from fastapi import status, HTTPException
import  jwt
from src.parameter import SECRET_KEY, ALGORITHM
from src.Stories.models import Stories
from src.Chapter.models import Chapter
from src.Activity.models import Activity
from src.Character.models import Character
from src.ChapterWiseUser.models import ChapterWiseUser


# def get_all_users(admin_token: str, db: Session, search: Optional[str] = None):
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

#         # Retrieve all user data if the user is an admin
#         # all_users = db.query(UserProfile).order_by(UserProfile.id.desc()).all()
#         all_users_query = db.query(UserProfile)

#         if search is not None:
#             all_users_query = all_users_query.filter(
#                 UserProfile.name.ilike(f"%{search}%"))

#         all_users = all_users_query.filter(
#             UserProfile.account_status == "Activate").order_by(UserProfile.id.desc()).all()
#         response = {
#             'status': 'true',
#             'message': "Data Received Successfully",
#             'data': all_users
#         }
#         return response

#     except jwt.ExpiredSignatureError:
#         return {"status": "false", "message": "Token has expired"}
#     except jwt.InvalidTokenError:
#         return {"status": "false", "message": "Invalid token"}
#     except InvalidToken:
#         return {"status": "false", "message": "Invalid or corrupted token"}

def get_all_users(admin_token: str, db: Session, search: Optional[str] = None):
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

        # Retrieve all user data if the user is an admin
        all_users_query = db.query(UserProfile)

        if search:
            all_users_query = all_users_query.filter(
                UserProfile.name.ilike(f"%{search}%"))

        all_users = all_users_query.filter(
            UserProfile.account_status == "Activate").order_by(UserProfile.id.desc()).all()

        return {
            'status': 'true',
            'message': "Data Received Successfully",
            'data': all_users
        }
    except jwt.InvalidTokenError:
        return {"status": "false", "message": "Invalid token"}
    except Exception as e:
        return {"status": "false", "message": f"An error occurred: {str(e)}"}


def get_all_block_users(admin_token: str, db: Session, search: Optional[str] = None):
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

        # Retrieve all user data if the user is an admin
        # all_users = db.query(UserProfile).order_by(UserProfile.id.desc()).all()
        all_users_query = db.query(UserProfile)

        if search is not None:
            all_users_query = all_users_query.filter(
                UserProfile.name.ilike(f"%{search}%"))

        all_users = all_users_query.filter(
            UserProfile.account_status == "Deactivate").order_by(UserProfile.id.desc()).all()
        response = {
            'status': 'true',
            'message': "Data Received Successfully",
            'data': all_users
        }
        return response

    except jwt.InvalidTokenError:
        return {"status": "false", "message": "Invalid token"}
    except Exception as e:
        return {"status": "false", "message": f"An error occurred: {str(e)}"}


def create(db: Session, user_profile_create: UserProfileCreate):
    email = user_profile_create.email
    phone = user_profile_create.phone_number
    existing_email_profiles = db.query(
        UserProfile).filter(UserProfile.email == email).all()
    if len(existing_email_profiles) > 0:
        return {'status': 'false', 'message': 'Email is already registered. Try another email'}

    existing_phone_profiles = db.query(UserProfile).filter(
        UserProfile.phone_number == phone).all()
    if phone and len(existing_phone_profiles) > 0:
        return {'status': 'false', 'message': 'Phone Number is already registered. Try another Phone Number'}

        # Create and add the new UserProfile
    db_user_profile = UserProfile(**user_profile_create.dict())
    db.add(db_user_profile)
    db.commit()
    db.refresh(db_user_profile)

    chapters = db.query(Chapter).all()

    for chapter in chapters:
        # Create a new ChapterWiseUser entry for each user and chapter
        new_entry = ChapterWiseUser(
            user_id=db_user_profile.id,
            chapter_id=chapter.id,
            stories_id=chapter.stories_id,
            read_status="0",
            read_date="1-1-2-2024"
        )
        db.add(new_entry)
        db.commit()

    response = {'status': 'true',
                'message': 'User Details Added Successfully',
                'data': db_user_profile}

    return response


def update(user_profile: UserProfile, db: Session, user_token: str):
    try:
        # Decode the JWT token
        payload = jwt.decode(user_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")

        # Prepare the update data
        user_profile_update = user_profile.dict(exclude_unset=True)

        # Update user profile in the database
        db.query(UserProfile).filter(UserProfile.id ==
                                     user_id).update(user_profile_update)
        db.commit()

        response = {
            'status': 'true',
            'message': "User Details Updated Successfully",
            'data': user_profile_update
        }
        return response

    except jwt.InvalidTokenError:
        return {"status": "false", "message": "Invalid token"}
    except Exception as e:
        return {"status": "false", "message": f"An error occurred: {str(e)}"}


def get_user_by_token(encrypted_token: str, db: Session):
    try:
        # Decode the JWT token
        payload = jwt.decode(encrypted_token, SECRET_KEY,
                             algorithms=[ALGORITHM])
        user_id = payload.get("user_id")

        # Retrieve user data from the database using the user_id
        user_data = db.query(UserProfile).filter(
            UserProfile.id == user_id).first()
        
        if not user_data:
            return {"status": 'false', 'message': "User not found"}

        return {
            'status': 'true',
            'message': 'User data retrieved successfully',
            'user': {
                'user_id': user_data.id,
                'email': user_data.email,
                'name': user_data.name,
                'password': user_data.password,
                'phone_number': user_data.phone_number,
                'account_status': user_data.account_status,
                'login_type': user_data.login_type,
                'expire_session_token': user_data.expire_session_token,
                'last_session_time': user_data.last_session_time,
                'session_token': user_data.session_token,
                'created_at': user_data.created_at,
                'updated_at': user_data.updated_at,
            }
        }
    except jwt.InvalidTokenError:
        return {"status": "false", "message": "Invalid token"}
    except Exception as e:
        return {"status": "false", "message": f"An error occurred: {str(e)}"}


def delete_user_by_token(user_token: str, db: Session):
    try:
        # Decode the JWT token
        payload = jwt.decode(user_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")

        user_details = db.query(UserProfile).filter(
            UserProfile.id == user_id).first()

        if not user_details:
            return {'status': 'false', 'message': "User Details not found"}

        db.delete(user_details)
        db.commit()

        response = {
            'status': 'true',
            'message': "User Details deleted successfully"
        }

        return response

    except jwt.InvalidTokenError:
        return {"status": "false", "message": "Invalid token"}
    except Exception as e:
        return {"status": "false", "message": f"An error occurred: {str(e)}"}


def delete_user_by_admin_token(admin_token: str, id: str, db: Session):
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

        user_details = db.query(UserProfile).filter(
            UserProfile.id == id).first()

        if not user_details:
            return {'status': 'false', 'message': "User Details not found"}

        db.query(ChapterWiseUser).filter(
            ChapterWiseUser.user_id == user_id).delete()

        db.delete(user_details)
        db.commit()

        response = {
            'status': 'true',
            'message': "User Details deleted successfully"
        }

        return response

    except jwt.InvalidTokenError:
        return {"status": "false", "message": "Invalid token"}
    except Exception as e:
        return {"status": "false", "message": f"An error occurred: {str(e)}"}


def update_reset_password(db: Session, password_data: UpdatePassword, user_token: str,):
    try:
        # Decode the JWT token
        payload = jwt.decode(user_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")

        # Retrieve user data from the database using the user_id
        user_data = db.query(UserProfile).filter(
            UserProfile.id == user_id).first()

        if not user_data:
            return {"status": 'false', 'message': "User not found"}

        # Update the user's password
        user_data.password = password_data.password
        db.commit()

        return {
            'status': 'true',
            'message': "User Password Updated Successfully"
        }

    except jwt.ExpiredSignatureError:
        return {"status": 'false', 'message': "Token has expired"}
    except jwt.InvalidTokenError:
        return {"status": 'false', 'message': "Invalid token"}


def update_reset_password_by_email(db: Session, password_data: UpdatePassword, email: str):

    # Retrieve user data from the database using the user_id
    user_data = db.query(UserProfile).filter(
        UserProfile.email == email).first()

    if not user_data:
        return {"status": 'false', 'message': "User not found"}

    # Update the user's password
    user_data.password = password_data.password
    db.commit()

    return {
        'status': 'true',
        'message': "User Password Updated Successfully"
    }


def update_account_status(db: Session, status_data: UpdateAccountStatus, admin_token: str):
    try:
        # Decode the JWT token
        payload = jwt.decode(admin_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        role = payload.get("role")

        update_user_id = status_data.user_id

        # Retrieve user data from the database using the user_id
        user_data = db.query(UserProfile).filter(
            UserProfile.id == user_id).first()

        if not user_data:
            return {"status": 'false', 'message': "User not found"}

        # Verify that the user is an admin
        if role != "admin":
            return {"status": 'false', 'message': "Access denied"}

        # Retrieve user data from the database using the user_id
        update_user_data = db.query(UserProfile).filter(
            UserProfile.id == update_user_id).first()

        if not update_user_data:
            return {"status": 'false', 'message': "User not found"}

        # Update the user's account status and status only if new values are provided
        if status_data.account_status is not None:
            update_user_data.account_status = status_data.account_status
        db.commit()

        return {
            'status': 'true',
            'message': "User Account Status Updated Successfully"
        }

    except jwt.ExpiredSignatureError:
        return {"status": 'false', 'message': "Token has expired"}
    except jwt.InvalidTokenError:
        return {"status": 'false', 'message': "Invalid token"}


def user_login(email: str, password: str, db: Session):
    user_data = db.query(UserProfile).filter(
        UserProfile.email == email).first()

    if not user_data:
        return {
            'status': "false",
            'message': "Invalid email or password"
        }

    # Assuming the password is hashed, use a hash check function
    if not user_data.password == password:  # Replace with proper password check if needed
        return {
            'status': "false",
            'message': "Invalid email or password"
        }

    # Set the role based on the email
    role = "admin" if email == "urc77@gmail.com" else "user"

    payload = {
        "user_id": user_data.id,
        "email": user_data.email,
        "role": role,
        "exp": datetime.utcnow() + timedelta(days=30)
    }

    # Encode the JWT token
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return {
        'status': "true",
        'message': "User Login Successfully",
        'token': token
    }

def get_user_by_email(email: str, db: Session):
    user = db.query(UserProfile).filter(UserProfile.email == email).first()

    if not user:
        return {'status': 'false', 'message': "User not found"}

    response = {'status': 'true',
                'message': "Data Recived Successfully", 'data': user}
    return response


def get_dashboard_count(admin_token: str, db: Session):
    try:
        # Decode the JWT token
        payload = jwt.decode(admin_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        role = payload.get("role")

        # Verify that the user is an admin
        if role != "admin":
            return {"status": 'false', 'message': "Access denied"}

        # Retrieve user data from the database using the user_id
        user_data = db.query(UserProfile).filter(
            UserProfile.id == user_id).first()

        if not user_data:
            return {"status": 'false', 'message': "User not found"}

        # Retrieve all user data if the user is an admin
        all_users = db.query(UserProfile).order_by(
            UserProfile.id.desc()).count()
        all_stories = db.query(Stories).order_by(Stories.id.desc()).count()
        all_chapters = db.query(Chapter).order_by(Chapter.id.desc()).count()
        all_activity = db.query(Activity).order_by(Activity.id.desc()).count()
        all_character = db.query(Character).order_by(
            Character.id.desc()).count()
        all_block_users = db.query(UserProfile).filter(
            UserProfile.account_status == "Deactivate").count()

        return {
            'status': 'true',
            'message': "Data Received Successfully",
            'no_of_users': all_users,
            'stories_posted': all_stories,
            'total_chapters_across_all_stories': all_chapters,
            'activities_listed': all_activity,
            'characters_posted': all_character,
            'avg_no_of_activities_per_story': int(all_activity / all_stories),
            'blocked_users': all_block_users
        }

    except jwt.ExpiredSignatureError:
        return {"status": 'false', 'message': "Token has expired"}
    except jwt.InvalidTokenError:
        return {"status": 'false', 'message': "Invalid token"}
