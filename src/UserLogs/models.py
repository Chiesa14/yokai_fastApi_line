from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, date
import pytz

def get_current_datetime():
    india_tz = pytz.timezone('Asia/Kolkata')
    return datetime.now(india_tz)

class UserLogsBase(SQLModel):
    user_id: int = Field(nullable=False)  # Foreign Key to UserProfile
    login_count: int = Field(default=1)  # Count of logins
    last_login_date: date = Field(nullable=False)  # Date of the last login

class UserLogs(UserLogsBase, table=True):
    __tablename__ = "user_logs"
    id: Optional[int] = Field(primary_key=True, nullable=False)
    timestamp: datetime = Field(default_factory=get_current_datetime, nullable=False)  # Optional if you want to keep the original timestamp
    ip_address: Optional[str] = Field(nullable=True)  # Optionally store the IP address for the log entry

# Classes for creating and reading user logs
class UserLogsCreate(SQLModel):
    user_id: int

class UserLogsRead(UserLogsBase):
    id: int
    timestamp: datetime
    ip_address: Optional[str]

