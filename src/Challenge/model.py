from sqlmodel import SQLModel, Field
from typing import Optional, List
from datetime import datetime
import pytz
from fastapi import FastAPI, Depends, APIRouter
from sqlmodel import Session

# Define the FastAPI app and router
app = FastAPI()
router = APIRouter()

def get_current_datetime():
    # Set the timezone to Kolkata, India
    kolkata_tz = pytz.timezone('Asia/Kolkata')
    return datetime.now(kolkata_tz)

class ChallengeBase(SQLModel):
    name: str = Field(nullable=False)
    description: str = Field(nullable=False)
    criteria: str = Field(nullable=False)
    reward: int = Field(nullable=False)
    badge_name: str = Field(nullable=False)
    badge_description: str = Field(nullable=False)
    badge_criteria: str = Field(nullable=False)
    badge_step_count: int = Field(nullable=False)
    badge_image_path: str = Field(nullable=False)
    badge_type: str = Field(nullable=False)

class Challenge(ChallengeBase, table=True):
    __tablename__ = "challenges"
    id: Optional[int] = Field(primary_key=True, nullable=False)
    isRewarded: bool = Field(default=False)

class ChallengeCreate(ChallengeBase):
    pass

class ChallengeRead(ChallengeBase):
    id: int


class UserChallengeBase(SQLModel):
    user_id: int = Field(nullable=False)
    challenge_id: int = Field(nullable=False)
    isRewarded: bool = Field(default=False)


class UserChallenge(UserChallengeBase, table=True):
    __tablename__ = "user_challenges"

    id: Optional[int] = Field(primary_key=True, nullable=False)



class UserChallengeCreate(UserChallengeBase):
    pass


class UserChallengeRead(UserChallengeBase):
    id: int
