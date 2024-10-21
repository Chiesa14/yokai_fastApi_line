from random import random
from sqlalchemy import func
from sqlmodel import Session
from.models import SentCompliment
from typing import Optional

from sqlmodel import Session, select
from .models import Compliment, CreateCompliment, SentCompliment
from datetime import datetime
from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage
import os


# line_bot_api=LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)

def response(status: bool, message: str, data: Optional[dict]=None)-> dict:
    
    return{
       'status': str(status).lower(),
       'message': message,
        'data': data
    
}
    
#CREATING A COMPLIMENT
    
def create_compliment(db: Session, compliment: CreateCompliment ) -> dict:
    db_compliment= Compliment(**compliment.dict())
    db.add(db_compliment)
    db.commit()
    db.refresh(db_compliment)
    return response(True, "Compliment Created Successfully", db_compliment)

# Getting the compliments

def get_compliments(db:Session) -> dict:
    
    stmt= select(Compliment)
    compliments= db.exec(stmt).all()
    return response(True,"Compliments Retrieved Successfully",compliments)
    
    
  


def get_sent_compliments(db: Session):
    return db.exec(select(SentCompliment)).all()  
# Getting a specific compliment
def get_compliment_by_id(db:Session, compliment_id:int) -> dict:
    stmt=select(Compliment).where(Compliment.id == compliment_id)
    compliment= db.exec(stmt).first()
    return response(True,f"Compliment with the ID {compliment_id} retrieved Successfully",compliment)
     


async def get_random_compliment(db: Session) -> Compliment:
    stmt = select(Compliment).order_by(func.random()).limit(1)
    return db.exec(stmt).first()
     
     
async def get_compliment_question(user_id: str) -> dict:
    
    compliment= await get_random_compliment()

    
    return {
        "compliment":compliment,
    
    }     
    
def get_random_friends(friends: list[str],count:int) -> list[str]:
    return random.sample(friends,count)
     
     
async def  send_compliment(sender_id: str, recipient_id:str):
    
    sent_compliment= SentCompliment(
        sender_id=sender_id,
        recipient_id=recipient_id,
     
        sent_at=datetime.utcnow()
    )
    # await save_sent_compliment(sent_compliment)
    
    await notify_recipient(recipient_id)
    
    return sent_compliment





async def notify_recipient(recipient_id:str,message: str):
    try:
    
    
        line_bot_api.push_message(
            recipient_id,
            TextSendMessage(text=f"You've received a compliment")
        )
    except Exception as e:
        print(f"Failed to send notification to {recipient_id}: {str(e)}")
    
    
def save_sent_compliment(db: Session, sent_compliment: SentCompliment):
    db.add(sent_compliment)
    db.commit()
    db.refresh(sent_compliment)
    return sent_compliment


def get_sent_compliments(db: Session):
    return db.exec(select(SentCompliment)).all()
    
    
    

       