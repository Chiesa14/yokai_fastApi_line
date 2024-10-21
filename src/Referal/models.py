from sqlmodel import SQLModel, Field, Relationship
from pydantic import BaseModel
from datetime import datetime
import pytz
from typing import Optional


def get_current_datetime():
    # Set the timezone to Kolkata, India
    kolkata_tz = pytz.timezone('Asia/Kolkata')
    now = datetime.now(kolkata_tz)
    return now


class ReferralCodeBase(SQLModel):
    referral_code: Optional[str] = Field(nullable=False, default=None)


class ReferralCode(ReferralCodeBase, table=True):
    __tablename__ = "referral_codes"

    id: Optional[int] = Field(primary_key=True, nullable=False)
    user_id: int = Field(foreign_key="user_profile.id", nullable=False)
    created_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
    updated_at: datetime = Field(default_factory=get_current_datetime, nullable=False)



class ReferralCodeCreate(ReferralCodeBase):
    user_id: int


class ReferralCodeRead(ReferralCodeBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime


class UpdateReferralCode(SQLModel):
    referral_code: Optional[str] = None
