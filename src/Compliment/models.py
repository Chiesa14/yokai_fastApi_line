
from typing import Optional
from pydantic import BaseModel
from sqlmodel import Field, SQLModel

from datetime import datetime 
 
class ComplimentBase(SQLModel):
    yokai_image: str
    title: str
    description: str
    story: str


class Compliment(ComplimentBase, table=True):
    __tablename__="compliments"
    id: Optional[int] = Field(primary_key=True, nullable=False)
    
    

class CreateCompliment(ComplimentBase) :
    pass
    
    
    

class SentComplimentBase(SQLModel):
    sender_id: str
    recipient_id: str
    sent_at: datetime = Field(default_factory=datetime.utcnow)
    
class SentCompliment(SentComplimentBase,table=True):
    __tablename__ = 'sent_compliments'
    id: Optional[int] = Field(default=None,primary_key=True)
           
    
class ComplimentResponse():
    compliment_text: str
    yokai_name: str
    blurred_preview: str  
    contact: str  
    delivery_status: str