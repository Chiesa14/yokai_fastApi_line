from sqlmodel import SQLModel,Field,Relationship
from pydantic import UUID4
from datetime import datetime,date
from typing import Optional,List
from pydantic import BaseModel
import pytz



def get_current_datetime():
    # Set the timezone to Madrid, Spain
    madrid_tz = pytz.timezone('Asia/Kolkata')

    # Get the current time in the specified timezone
    now = datetime.now(madrid_tz)

    return now

class UserProfileBase(SQLModel):
    name : Optional[str] = Field(nullable=False,default=None)
    email : str = Field(nullable=False,default=None)
    password : Optional[str] = Field(nullable=True,default=None)
    phone_number : Optional[str] = Field(nullable=True,default=None)
    login_type : Optional[str] = Field(nullable=True,default=None)


class UserProfile(UserProfileBase,table = True):
    __tablename__ = "user_profile"
    id : Optional[int] = Field(primary_key=True, nullable=False)
    account_status : Optional[str] = Field(nullable=False,default="Activate")
    created_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
    updated_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
    session_token : Optional[str] = Field(nullable=True,default=None)
    last_session_time : Optional[str] = Field(nullable=True,default=None)
    expire_session_token : Optional[str] = Field(nullable=True,default=None)


class UserProfileCreate(UserProfileBase):
    pass

class UserProfileRead(UserProfileBase):
    id : int

class UpdatePassword(SQLModel):
    password: Optional[str] = None

class UpdateAccountStatus(SQLModel):
    user_id: Optional[str] = None
    account_status: Optional[str] = None