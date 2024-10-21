from typing import List, Optional
from sqlmodel import Session, select
from .models import TodoType, TodoTypeCreate, UserTodo, UserTodoCreate

# Utility function for creating responses
def create_response(status: bool, message: str, data: Optional[dict] = None) -> dict:
    return {
        'status': str(status).lower(),
        'message': message,
        'data': data
    }

# TodoType Services
def create_todo_type(db: Session, todo_type: TodoTypeCreate) -> dict:
    db_todo_type = TodoType.from_orm(todo_type)
    db.add(db_todo_type)
    db.commit()
    db.refresh(db_todo_type)
    return create_response(True, "Todo Type Created Successfully", db_todo_type)

def get_todo_type(db: Session, todo_type_id: int) -> dict:
    stmt = select(TodoType).where(TodoType.id == todo_type_id)
    todo_type = db.exec(stmt).first()
    if todo_type:
        return create_response(True, "Todo Type Retrieved Successfully", todo_type)
    return create_response(False, "Todo Type Not Found")

def get_todo_types(db: Session) -> dict:
    stmt = select(TodoType)
    todo_types = db.exec(stmt).all()
    return create_response(True, "Todo Types Retrieved Successfully", todo_types)

def update_todo_type(db: Session, todo_type_id: int, todo_type_update: TodoTypeCreate) -> dict:
    stmt = select(TodoType).where(TodoType.id == todo_type_id)
    db_todo_type = db.exec(stmt).first()
    if db_todo_type:
        db_todo_type.type = todo_type_update.type
        db_todo_type.description = todo_type_update.description
        db_todo_type.target_count = todo_type_update.target_count
        db.add(db_todo_type)
        db.commit()
        db.refresh(db_todo_type)
        return create_response(True, "Todo Type Updated Successfully", db_todo_type)
    return create_response(False, "Todo Type Not Found")

def delete_todo_type(db: Session, todo_type_id: int) -> dict:
    stmt = select(TodoType).where(TodoType.id == todo_type_id)
    db_todo_type = db.exec(stmt).first()
    if db_todo_type:
        db.delete(db_todo_type)
        db.commit()
        return create_response(True, "Todo Type Deleted Successfully")
    return create_response(False, "Todo Type Not Found")

# UserTodo Services
def create_user_todo(db: Session, user_todo: UserTodoCreate) -> dict:
    db_user_todo = UserTodo.from_orm(user_todo)
    db.add(db_user_todo)
    db.commit()
    db.refresh(db_user_todo)
    return create_response(True, "User Todo Created Successfully", db_user_todo)

def get_user_todo(db: Session, user_todo_id: int) -> dict:
    stmt = select(UserTodo).where(UserTodo.id == user_todo_id)
    user_todo = db.exec(stmt).first()
    if user_todo:
        return create_response(True, "User Todo Retrieved Successfully", user_todo)
    return create_response(False, "User Todo Not Found")

def get_user_todos(db: Session, user_id: int) -> dict:
    stmt = select(UserTodo).where(UserTodo.user_id == user_id)
    user_todos = db.exec(stmt).all()
    return create_response(True, "User Todos Retrieved Successfully", user_todos)

def update_user_todo(db: Session, user_todo_id: int, user_todo_update: UserTodoCreate) -> dict:
    stmt = select(UserTodo).where(UserTodo.id == user_todo_id)
    db_user_todo = db.exec(stmt).first()
    if db_user_todo:
        db_user_todo.completed_count = user_todo_update.completed_count
        db_user_todo.is_completed = user_todo_update.is_completed
        db.add(db_user_todo)
        db.commit()
        db.refresh(db_user_todo)
        return create_response(True, "User Todo Updated Successfully", db_user_todo)
    return create_response(False, "User Todo Not Found")

def delete_user_todo(db: Session, user_todo_id: int) -> dict:
    stmt = select(UserTodo).where(UserTodo.id == user_todo_id)
    db_user_todo = db.exec(stmt).first()
    if db_user_todo:
        db.delete(db_user_todo)
        db.commit()
        return create_response(True, "User Todo Deleted Successfully")
    return create_response(False, "User Todo Not Found")
