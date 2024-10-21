from sqlmodel import SQLModel,Field,Relationship
from pydantic import UUID4
from datetime import datetime,date
from typing import Optional,List
from pydantic import BaseModel
import pytz

# TodoType Table
class TodoTypeBase(SQLModel):
    type: str = Field(nullable=False)
    description: str = Field(nullable=False)
    target_count: int = Field(nullable=False)
    badge: str = Field(nullable=False)  # New field for badge

class TodoType(TodoTypeBase, table=True):
    __tablename__ = "todo_type"
    id: Optional[int] = Field(primary_key=True, nullable=False,default=None)

class TodoTypeCreate(TodoTypeBase):
    pass

class TodoTypeRead(TodoTypeBase):
    id: int

# UserTodo Table
class UserTodoBase(SQLModel):
    user_id: int = Field(foreign_key="user_profile.id", nullable=False)
    todo_type_id: int = Field(foreign_key="todo_type.id", nullable=False)
    completed_count: int = Field(default=0, nullable=False)
    is_completed: bool = Field(default=False, nullable=False)

class UserTodo(UserTodoBase, table=True):
    __tablename__ = "user_todo"
    id: Optional[int] = Field(primary_key=True, nullable=False)

class UserTodoCreate(UserTodoBase):
    pass

class UserTodoRead(UserTodoBase):
    id: int