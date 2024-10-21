from sqlmodel import SQLModel, Field
from typing import Optional
from pydantic import validator
from datetime import datetime
import pytz

def get_current_datetime():
    india_tz = pytz.timezone('Asia/Kolkata')
    return datetime.now(india_tz)

class MoodBase(SQLModel):
    user_id: str = Field(nullable=False)  # ID of the user
    mood_level: float = Field(nullable=False)  # Mood level (0 to 1)
    mood_gif: int = Field(nullable=False)  # Mood GIF range (0 to 5)
    date: datetime = Field(default_factory=get_current_datetime)  # Date of the entry

    @staticmethod
    def validate_mood_gif(value):
        if value < 0 or value > 5:
            raise ValueError("mood_gif must be between 0 and 5")
        return value

class Mood(MoodBase, table=True):
    __tablename__ = "mood"
    id: Optional[int] = Field(primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
    updated_at: datetime = Field(default_factory=get_current_datetime, nullable=False)

class MoodCreate(MoodBase):
    pass

class MoodRead(MoodBase):
    id: int

class MoodUpdate(SQLModel):
    mood_level: Optional[float] = None
    mood_gif: Optional[int] = None
