from typing import List
from fastapi import APIRouter, Depends
from sqlmodel import Session
from src.database import get_db
from .model import BadgeCreate
from .service import (
    create_badge,
    get_badge,
    get_all_badges,
    update_badge,
    delete_badge
)

router = APIRouter()

@router.post("/create-badge")
def create_badge_view(badge_create: BadgeCreate, db: Session = Depends(get_db)):
    return create_badge(db=db, badge_create=badge_create)

@router.get("/get-badge/{badge_id}")
def read_badge(badge_id: int, db: Session = Depends(get_db)):
    return get_badge(db=db, badge_id=badge_id)

@router.get("/get-all-badges")
def read_all_badges(db: Session = Depends(get_db)):
    return get_all_badges(db=db)

@router.put("/update-badge/{badge_id}")
def update_badge_view(badge_id: int, badge_update: BadgeCreate, db: Session = Depends(get_db)):
    return update_badge(db=db, badge_id=badge_id, badge_update=badge_update)

@router.delete("/delete-badge/{badge_id}")
def delete_badge_view(badge_id: int, db: Session = Depends(get_db)):
    return delete_badge(db=db, badge_id=badge_id)
