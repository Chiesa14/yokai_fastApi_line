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

class ActivityDetailsBase(SQLModel):
    activity_id : Optional[str] = Field(nullable=False,default=None)
    sr_no : Optional[str] = Field(nullable=False,default=None)
    question : Optional[str] = Field(nullable=False,default=None)
    option_a : Optional[str] = Field(nullable=False,default=None)
    option_b : Optional[str] = Field(nullable=False,default=None)
    option_c : Optional[str] = Field(nullable=False,default=None)
    option_d : Optional[str] = Field(nullable=False,default=None)
    explation : Optional[str] = Field(nullable=False,default=None)
    correct_answer : Optional[str] = Field(nullable=False,default=None)
    image : Optional[str] = Field(nullable=False,default=None)

class ActivityDetails(ActivityDetailsBase,table = True):
    __tablename__ = "activity_details"
    id : Optional[int] = Field(primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
    updated_at: datetime = Field(default_factory=get_current_datetime, nullable=False)

class ActivityDetailsCreate(ActivityDetailsBase):
    pass

class ActivityDetailsRead(ActivityDetailsBase):
    id : int