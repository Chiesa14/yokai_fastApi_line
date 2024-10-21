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

class CharacterChatBase(SQLModel):
    user_id : Optional[str] = Field(nullable=False,default=None)
    character_id : Optional[str] = Field(nullable=False,default=None)
    question : Optional[str] = Field(nullable=False,default=None)
    answer : Optional[str] = Field(nullable=False,default=None)

class CharacterChat(CharacterChatBase,table = True):
    __tablename__ = "character_chat"
    id : Optional[int] = Field(primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
    updated_at: datetime = Field(default_factory=get_current_datetime, nullable=False)

class CharacterChatCreate(CharacterChatBase):
    pass

class CharacterChatRead(CharacterChatBase):
    id : int
    
    
class BatchBase(SQLModel):
    user_id : Optional[str] = Field(nullable=False,default=None)
    level : Optional[str] = Field(nullable=False,default=None)
    count : Optional[str] = Field(nullable=False,default=None)
    last_hit_time : Optional[str] = Field(nullable=False,default=None)

class Batch(BatchBase,table = True):
    __tablename__ = "batch"
    id : Optional[int] = Field(primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
    updated_at: datetime = Field(default_factory=get_current_datetime, nullable=False)

class BatchCreate(BatchBase):
    pass

class BatchRead(BatchBase):
    id : int     