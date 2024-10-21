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

class ChapterWiseUserBase(SQLModel):
    stories_id : Optional[str] = Field(nullable=False,default=None)
    chapter_id : Optional[str] = Field(nullable=False,default=None)
    user_id : Optional[str] = Field(nullable=False,default=None)
    read_status : Optional[str] = Field(nullable=False,default=None)
    read_date : Optional[str] = Field(nullable=False,default=None)

class ChapterWiseUser(ChapterWiseUserBase,table = True):
    __tablename__ = "chapter_wise_user"
    id : Optional[int] = Field(primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
    updated_at: datetime = Field(default_factory=get_current_datetime, nullable=False)

class ChapterWiseUserCreate(ChapterWiseUserBase):
    pass

class ChapterWiseUserRead(ChapterWiseUserBase):
    id : int
    
class UpdateReadStatus(SQLModel):
    read_status: Optional[str] = None