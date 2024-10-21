from xml.sax import handler
from fastapi import Depends, FastAPI, Request,HTTPException
from sqlmodel import Session, SQLModel
import urllib
from src.database import SessionLocal, get_db, engine, Base
from src.api import api_router
import logging
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from linebot.exceptions import InvalidSignatureError
import requests
Base.metadata.create_all(engine)
db = SessionLocal()


app = FastAPI()

logger = logging.getLogger()
logger.setLevel(logging.INFO)

origins = [
    "https://surfhealthprogram.com",
    "http://surfhealthprogram.com",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# we add all API routes to the Web API framework
app.include_router(api_router, prefix="/v1")

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(bind=engine)
@app.get("/")
async def root():
    return {"message": "Hello World"}



LINE_AUTH_URL="https://access.line.me/oauth2/v2.1/authorize"
CHANNEL_ID=os.getenv("LINE_CHANNEL_ID") 
REDIRECT_URI= os.getenv("LINE_REDIRECT_URI")
SCOPE= "profile openid"

LINE_TOKEN_URL="https://api.line.me/oauth2/v2.1/token"
LINE_CHANNEL_SECRET=os.getenv("CHANNEL_SECRET")


@app.get("/authorize")
async def authorize():
    params= {
        "response_type":"code",
        "client_id":CHANNEL_ID,
        "redirect_uri":REDIRECT_URI,
        "scope":SCOPE,
        "state":"37763ybhddhd82dj"
    }
    url= LINE_AUTH_URL + "?" + urllib.parse.urlencode(params)
    return {"redirect_url":url}


# Handle the callback and exchange authorization code for ACCESS_TOKEN

@app.get("/callback/")
async def callback(code: str):
    data={
        "grant_type":"authorization_code",
        "code":code,
        "client_id":CHANNEL_ID,
        "client_secret":LINE_CHANNEL_SECRET,
        "redirect_uri":REDIRECT_URI
    }
    
    headers ={
        "Content-Type": "application/json"
    }
    response = requests.post(LINE_TOKEN_URL,data=data,headers=headers)
    if response.status_code !=200 :
        raise HTTPException(status_code=response.status_code,detail="Failed to get the access token")
    
    token_data=response.json()
    access_token=token_data["access_token"]
    logging.info({"access_token":access_token})
    return {"access_token":access_token}
# Endpoint to handle events

@app.post("/webhook")
async def webhook(request:Request):
    signature= request.headers["X-Line-Signature"]
    body = await request.body()
    try:
        handler.handle(body.decode("utf-8"), signature)
    except InvalidSignatureError:    
        return "Invalid signature"
    
    return "OK"
    
    

# @handler.add(MessageEvent,message=TextMessage)
# async def handle_message(event):
        
#     user_id = event.source.user_id
#     message_text= event.message.text.lower()
    
#     if message_text == "send compliment":
#         compliment_question = await get_compliment_question(user_id)
#         compliment_text = compliment_question['compliment'].description
#         friend_options = compliment_question['friendOptions']

#         options_message = f'Here’s a compliment: "{compliment_text}". Who would you like to send it to?'
#         friend_names = ', '.join(friend_options)

#         line_bot_api.reply_message(
#             event.reply_token,
#             TextSendMessage(text=f'{options_message}\nOptions: {friend_names}')
#         )
        
#     elif message_text.startswith("select friend"):
#         selected_friend = message_text.split("select friend")[1].strip()

#         # Send the compliment to the selected friend
#         sent_compliment = await send_compliment(user_id, selected_friend, compliment_question['compliment'].id)

#         confirmation_message = f'Your compliment has been sent to {selected_friend}.'
#         line_bot_api.reply_message(
#             event.reply_token,
#             TextSendMessage(text=confirmation_message)
#         )
 