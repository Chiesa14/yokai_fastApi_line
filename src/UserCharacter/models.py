from sqlmodel import SQLModel,Field,Relationship
from pydantic import UUID4
from datetime import datetime,date
from typing import Optional,List
from pydantic import BaseModel
from sqlalchemy import Column,DateTime
import pytz

def get_current_datetime():
    # Set the timezone to Madrid, Spain
    india_tz = pytz.timezone('Asia/Kolkata')
    
    # Get the current time in the specified timezone
    now = datetime.now(india_tz)
    
    return now

class UsercharacterBase(SQLModel):
    character_id : Optional[str] = Field(nullable=False,default=None)
    user_id : Optional[str] = Field(nullable=False,default=None)

class Usercharacter(UsercharacterBase,table = True):
    __tablename__ = "user_character"
    id : Optional[int] = Field(primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
    updated_at: datetime = Field(default_factory=get_current_datetime, nullable=False)

class UsercharacterCreate(UsercharacterBase):
    pass

class UsercharacterRead(UsercharacterBase):
    id : int     