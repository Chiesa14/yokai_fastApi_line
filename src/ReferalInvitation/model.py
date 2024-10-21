import pytz
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional


def get_current_datetime():
    # Set the timezone to Kolkata, India
    kolkata_tz = pytz.timezone('Asia/Kolkata')
    now = datetime.now(kolkata_tz)
    return now

class InvitationBase(SQLModel):
    referral_code: str = Field(nullable=False)
    invite_count: int = Field(default=0)

class Invitation(InvitationBase, table=True):
    __tablename__ = "referral_invitations"

    id: Optional[int] = Field(primary_key=True, nullable=False)
    user_id: int = Field(foreign_key="user_profile.id", nullable=False)
    created_at: datetime = Field(default_factory=get_current_datetime, nullable=False)
    updated_at: datetime = Field(default_factory=get_current_datetime, nullable=False)

class InvitationCreate(InvitationBase):
    user_id: int

class InvitationRead(InvitationBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
