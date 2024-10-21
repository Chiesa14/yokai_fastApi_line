from sqlmodel import Session
from .model import Badge, BadgeCreate

def create_badge(db: Session, badge_create: BadgeCreate):
    badge = Badge(**badge_create.dict())
    db.add(badge)
    db.commit()
    db.refresh(badge)
    return {
        'status': 'true',
        'message': 'Badge created successfully.',
        'data': badge
    }

def get_badge(db: Session, badge_id: int):
    badge = db.query(Badge).filter(Badge.id == badge_id).first()
    if badge:
        return {
            'status': 'true',
            'message': 'Badge retrieved successfully.',
            'data': badge
        }
    return {
        'status': 'false',
        'message': 'Badge not found.',
        'data': None
    }

def get_all_badges(db: Session):
    badges = db.query(Badge).all()
    return {
        'status': 'true',
        'message': 'Badges retrieved successfully.',
        'data': badges
    }

def update_badge(db: Session, badge_id: int, badge_update: BadgeCreate):
    badge = db.query(Badge).filter(Badge.id == badge_id).first()
    if badge:
        # Update only the fields provided in the request
        for key, value in badge_update.dict(exclude_unset=True).items():
            setattr(badge, key, value)
        db.commit()
        db.refresh(badge)
        return {
            'status': 'true',
            'message': 'Badge updated successfully.',
            'data': badge
        }
    return {
        'status': 'false',
        'message': 'Badge not found.',
        'data': None
    }

def delete_badge(db: Session, badge_id: int):
    badge = db.query(Badge).filter(Badge.id == badge_id).first()
    if badge:
        db.delete(badge)
        db.commit()
        return {
            'status': 'true',
            'message': 'Badge deleted successfully.',
            'data': None
        }
    return {
        'status': 'false',
        'message': 'Badge not found.',
        'data': None
    }
