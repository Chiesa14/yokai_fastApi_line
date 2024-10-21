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

class ChapterBase(SQLModel):
    stories_id : Optional[str] = Field(nullable=False,default=None)
    name : Optional[str] = Field(nullable=False,default=None)
    chapter_no : Optional[str] = Field(nullable=False,default=None)
    chapter_document_english : Optional[str] = Field(nullable=True,default=None)
    chapter_document_japanese : Optional[str] = Field(nullable=True,default=None)

class Chapter(ChapterBase,table = True):
    __tablename__ = "chapter"
    id : Optional[int] = Field(primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
    updated_at: datetime = Field(default_factory=get_current_datetime, nullable=False)

class ChapterCreate(ChapterBase):
    pass

class ChapterRead(ChapterBase):
    id : int