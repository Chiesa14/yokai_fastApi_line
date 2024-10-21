from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import pytz

def get_current_datetime():
    india_tz = pytz.timezone('Asia/Kolkata')
    return datetime.now(india_tz)

class UserDevicesBase(SQLModel):
    user_id: int = Field(nullable=False)
    device_id: str = Field(nullable=False, unique=True)
    device_name: str = Field(nullable=False)
    ip_address: Optional[str] = Field(nullable=True)
    login_time: datetime = Field(default_factory=get_current_datetime, nullable=False)
    last_seen: datetime = Field(default_factory=get_current_datetime, nullable=False)

class UserDevices(UserDevicesBase, table=True):
    __tablename__ = "user_devices"
    id: Optional[int] = Field(primary_key=True, nullable=False)

class UserDevicesCreate(SQLModel):
    user_id: int
    device_id: str
    device_name: str
    ip_address: Optional[str] = None

class UserDevicesRead(UserDevicesBase):
    id: int

