from sqlmodel import SQLModel,Field,Relationship
from pydantic import UUID4
from datetime import datetime,date
from typing import Optional,List
from pydantic import BaseModel
from sqlalchemy import Column,DateTime
import pytz

def get_current_datetime():
   # Set the timezone to India (Asia/Kolkata)
    india_tz = pytz.timezone('Asia/Kolkata')
    
    # Get the current time in the specified timezone
    now = datetime.now(india_tz)
    
    return now

class ActivityBase(SQLModel):
    story_id : Optional[str] = Field(nullable=False,default=None)
    chapter_id : Optional[str] = Field(nullable=False,default=None)
    title : Optional[str] = Field(nullable=False,default=None)
    time : Optional[str] = Field(nullable=False,default=None)
    short_description : Optional[str] = Field(nullable=False, default=None)
    image : Optional[str] = Field(nullable=False,default=None)
    audio : Optional[str] = Field(nullable=True,default=None)
    activity_image : Optional[str] = Field(nullable=False,default=None)
    document_english : Optional[str] = Field(nullable=False,default=None)
    document_japanese : Optional[str] = Field(nullable=True,default=None)
    end_image : Optional[str] = Field(nullable=False,default=None)

class Activity(ActivityBase,table = True):
    __tablename__ = "activity"
    id : Optional[int] = Field(primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
    updated_at: datetime = Field(default_factory=get_current_datetime, nullable=False)

class ActivityCreate(ActivityBase):
    pass

class ActivityRead(ActivityBase):
    id : int