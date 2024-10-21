from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Header, Body, UploadFile, File, Request
from sqlmodel import Session
from src.database import get_db
from src.UserProfile.models import UserProfile, UserProfileCreate, UpdatePassword, UpdateAccountStatus
from src.UserProfile.service import create, get_all_users, get_user_by_token, update, delete_user_by_token, update_reset_password, user_login, update_account_status, delete_user_by_admin_token,get_all_block_users,get_user_by_email,update_reset_password_by_email,get_dashboard_count
import os
from datetime import datetime
from moviepy.editor import VideoFileClip

router = APIRouter()

@router.get("/getalluser")
def read_all_user_details(admin_token: str = Header(None, alias="AdminToken"), db: Session = Depends(get_db), search:Optional[str] = None):
    return get_all_users(admin_token=admin_token, db=db, search=search)

@router.get("/getallblockuser")
def read_all_block_users(admin_token: str = Header(None, alias="AdminToken"), db: Session = Depends(get_db), search:Optional[str] = None):
    return get_all_block_users(admin_token=admin_token, db=db, search=search)

@router.post("/createUser")
def create_user_details(user_profile_create: UserProfileCreate, db: Session = Depends(get_db)):
    return create(db=db, user_profile_create=user_profile_create)


@router.get("/getUserByToken")
def read_user_by_token(user_token: str = Header(None, alias="UserToken"), db: Session = Depends(get_db)):
    return get_user_by_token(encrypted_token=user_token, db=db)


@router.put("/updateUser")
def update_user_details(user_profile: UserProfileCreate, db: Session = Depends(get_db),user_token: str = Header(None, alias="UserToken")):
    return update(db=db, user_profile=user_profile, user_token=user_token,)


@router.delete("/deleteUser")
def delete_user_details_by_token(user_token: str = Header(None, alias="UserToken"), db: Session = Depends(get_db)):
    return delete_user_by_token(user_token=user_token, db=db)

@router.delete("/delete-User-By-Admin")
def delete_user_details_by_token(id:str, admin_token: str = Header(None, alias="AdminToken"), db: Session = Depends(get_db)):
    return delete_user_by_admin_token(admin_token=admin_token, id=id, db=db)

@router.put("/updatepassword")
def update_reset_password_route(
    password_data: UpdatePassword,
    db: Session = Depends(get_db),
    user_token: str = Header(None, alias="UserToken"),
    
):
    return update_reset_password(db=db, password_data=password_data, user_token=user_token) 

@router.put("/update-password-by-email/{email}")
def update_reset_password_by_email_route(
    email : str,
    password_data: UpdatePassword,
    db: Session = Depends(get_db) 
    
):
    return update_reset_password_by_email(db=db, password_data=password_data, email=email)

@router.put("/update-account-status")
def update_account_status_route(
    status_data: UpdateAccountStatus,
    db: Session = Depends(get_db),
    admin_token: str = Header(None, alias="AdminToken")
    
):
    return update_account_status(db=db, status_data=status_data, admin_token=admin_token) 


@router.post("/userLogin")
def user_login_view(
        email: str = Body(...),
        password: str = Body(...),
        db: Session = Depends(get_db)
):
    return user_login(email=email, password=password, db=db) 

@router.post("/upload-document/")
async def upload_images(request: Request, images: List[UploadFile] = File(...)):
    try:
        base_url = str(request.base_url)
        if not os.path.exists("uploads"):
            os.makedirs("uploads")

        image_urls = []

        for image in images:
            current_datetime = datetime.now().strftime("%Y%m%d%H%M%S")
            # Replace spaces in filename with underscores
            filename = image.filename.replace(" ", "_")
            image_path = os.path.join("uploads", f"{current_datetime}_{filename}")

            with open(image_path, "wb") as image_file:
                image_file.write(image.file.read())

            image_url = f"{base_url}/uploads/{current_datetime}_{filename}"
            
            image_info = {"url": image_url.replace(str(request.base_url), "")}

            if image.content_type.startswith("video/"):
                # Calculate the duration of the video
                video_clip = VideoFileClip(image_path)
                duration = int(video_clip.duration)
                video_clip.close()

                # Format duration in HH:MM:SS
                hours, remainder = divmod(duration, 3600)
                minutes, seconds = divmod(remainder, 60)
                duration_formatted = f"{hours:02}:{minutes:02}:{seconds:02}"

                image_info["duration"] = duration_formatted

            image_urls.append(image_info)

        return {"image_urls": image_urls}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/getuserbyemail/{email}")
def read_user_by_email(email: str, db: Session = Depends(get_db)):
    return get_user_by_email(email=email, db=db)

@router.get("/get-dashboard-count")
def read_dashboard_count(admin_token: str = Header(None, alias="AdminToken"), db: Session = Depends(get_db)):
    return get_dashboard_count(admin_token=admin_token, db=db)    