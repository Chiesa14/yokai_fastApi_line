from fastapi import FastAPI, Depends, HTTPException, APIRouter
from sqlmodel import Session
from .models import TodoTypeCreate, UserTodoCreate
from src.Todo.service import  (
    create_todo_type,
    get_todo_type,
    get_todo_types,
    update_todo_type,
    delete_todo_type,
    create_user_todo,
    get_user_todo,
    get_user_todos,
    update_user_todo,
    delete_user_todo,
)
from src.database import get_db

router = APIRouter()

# TodoType Endpoints
@router.post("/todo-types/")
def create_todo_type_endpoint(todo_type: TodoTypeCreate, db: Session = Depends(get_db)):
    return create_todo_type(db, todo_type)

@router.get("/todo-types/{todo_type_id}")
def read_todo_type(todo_type_id: int, db: Session = Depends(get_db)):
    todo_type = get_todo_type(db, todo_type_id)
    if todo_type is None:
        raise HTTPException(status_code=404, detail="TodoType not found")
    return todo_type

@router.get("/todo-types/")
def read_todo_types(db: Session = Depends(get_db)):
    return get_todo_types(db)

@router.put("/todo-types/{todo_type_id}")
def update_todo_type_endpoint(todo_type_id: int, todo_type_update: TodoTypeCreate, db: Session = Depends(get_db)):
    updated_todo_type = update_todo_type(db, todo_type_id, todo_type_update)
    if updated_todo_type is None:
        raise HTTPException(status_code=404, detail="TodoType not found")
    return updated_todo_type

@router.delete("/todo-types/{todo_type_id}")
def delete_todo_type_endpoint(todo_type_id: int, db: Session = Depends(get_db)):
    success = delete_todo_type(db, todo_type_id)
    if not success:
        raise HTTPException(status_code=404, detail="TodoType not found")
    return {"detail": "TodoType deleted"}

# UserTodo Endpoints
@router.post("/user-todos/")
def create_user_todo_endpoint(user_todo: UserTodoCreate, db: Session = Depends(get_db)):
    return create_user_todo(db, user_todo)

@router.get("/user-todos/{user_todo_id}")
def read_user_todo(user_todo_id: int, db: Session = Depends(get_db)):
    user_todo = get_user_todo(db, user_todo_id)
    if user_todo is None:
        raise HTTPException(status_code=404, detail="UserTodo not found")
    return user_todo

@router.get("/user-todos/user/{user_id}")
def read_user_todos(user_id: int, db: Session = Depends(get_db)):
    return get_user_todos(db, user_id)

@router.put("/user-todos/{user_todo_id}")
def update_user_todo_endpoint(user_todo_id: int, user_todo_update: UserTodoCreate, db: Session = Depends(get_db)):
    updated_user_todo = update_user_todo(db, user_todo_id, user_todo_update)
    if updated_user_todo is None:
        raise HTTPException(status_code=404, detail="UserTodo not found")
    return updated_user_todo

@router.delete("/user-todos/{user_todo_id}")
def delete_user_todo_endpoint(user_todo_id: int, db: Session = Depends(get_db)):
    success = delete_user_todo(db, user_todo_id)
    if not success:
        raise HTTPException(status_code=404, detail="UserTodo not found")
    return {"detail": "UserTodo deleted"}

