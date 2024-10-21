from sqlmodel import SQLModel, Field
from typing import Optional

class BadgeBase(SQLModel):
    name: str = Field(nullable=False, max_length=100)  # Name of the badge
    description: str = Field(nullable=False, max_length=255)  # Description of the badge
    criteria: str = Field(nullable=False, max_length=255)  # Criteria to earn the badge
    step_count: int = Field(nullable=False)  # The number of steps required to earn the badge
    type: str = Field(nullable=False, max_length=50)  # Type of the badge (e.g., "login", "share", etc.)

class Badge(BadgeBase, table=True):
    __tablename__ = "badges"
    id: Optional[int] = Field(primary_key=True, nullable=False)

class BadgeCreate(SQLModel):
    name: str
    description: str
    criteria: str
    step_count: int
    type: str

class BadgeRead(BadgeBase):
    id: int
