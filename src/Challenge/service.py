from typing import List, Optional
from sqlmodel import Session, select
from .model import Challenge, ChallengeCreate, UserChallenge, UserChallengeCreate


# Utility function for creating responses
def create_response(status: bool, message: str, data: Optional[dict] = None) -> dict:
    return {
        'status': str(status).lower(),
        'message': message,
        'data': data
    }

# Challenge Services
def create_challenge(db: Session, challenge: ChallengeCreate) -> dict:
    # Create a new Challenge instance from ChallengeCreate
    db_challenge = Challenge(**challenge.dict())
    db.add(db_challenge)
    db.commit()
    db.refresh(db_challenge)
    return create_response(True, "Challenge Created Successfully", db_challenge)


def get_challenge(db: Session, challenge_id: int) -> dict:
    stmt = select(Challenge).where(Challenge.id == challenge_id)
    challenge = db.exec(stmt).first()
    if challenge:
        return create_response(True, "Challenge Retrieved Successfully", challenge)
    return create_response(False, "Challenge Not Found")

def get_challenges(db: Session) -> dict:
    stmt= select(Challenge)
    challenges = db.exec(stmt).all()
    return create_response(True, "Challenges Retrieved Successfully", challenges)

def update_challenge(db: Session, challenge_id: int, challenge_update: ChallengeCreate) -> dict:
    stmt = select(Challenge).where(Challenge.id == challenge_id)
    db_challenge = db.exec(stmt).first()
    if db_challenge:
        db_challenge.name = challenge_update.name
        db_challenge.description = challenge_update.description
        db_challenge.criteria = challenge_update.criteria
        db_challenge.reward = challenge_update.reward
        db_challenge.badge_name = challenge_update.badge_name
        db_challenge.badge_description = challenge_update.badge_description
        db_challenge.badge_criteria = challenge_update.badge_criteria
        db_challenge.badge_step_count = challenge_update.badge_step_count
        db_challenge.badge_image_path = challenge_update.badge_image_path
        db_challenge.badge_type = challenge_update.badge_type
        db.add(db_challenge)
        db.commit()
        db.refresh(db_challenge)
        return create_response(True, "Challenge Updated Successfully", db_challenge)
    return create_response(False, "Challenge Not Found")

def delete_challenge(db: Session, challenge_id: int) -> dict:
    stmt = select(Challenge).where(Challenge.id == challenge_id)
    db_challenge = db.exec(stmt).first()
    if db_challenge:
        db.delete(db_challenge)
        db.commit()
        return create_response(True, "Challenge Deleted Successfully")
    return create_response(False, "Challenge Not Found")

# UserChallenge Services
def create_user_challenge(db: Session, user_challenge: UserChallengeCreate) -> dict:
    db_user_challenge = UserChallenge.from_orm(user_challenge)
    db.add(db_user_challenge)
    db.commit()
    db.refresh(db_user_challenge)
    return create_response(True, "User Challenge Created Successfully", db_user_challenge)

def get_user_challenge(db: Session, user_challenge_id: int) -> dict:
    stmt = select(UserChallenge).where(UserChallenge.id == user_challenge_id)
    user_challenge = db.exec(stmt).first()
    if user_challenge:
        return create_response(True, "User Challenge Retrieved Successfully", user_challenge)
    return create_response(False, "User Challenge Not Found")

def get_user_challenges(db: Session, user_id: int) -> dict:
    stmt = select(UserChallenge).where(UserChallenge.user_id == user_id)
    user_challenges = db.exec(stmt).all()
    return create_response(True, "User Challenges Retrieved Successfully", user_challenges)

def update_user_challenge(db: Session, user_challenge_id: int, user_challenge_update: UserChallengeCreate) -> dict:
    stmt = select(UserChallenge).where(UserChallenge.id == user_challenge_id)
    db_user_challenge = db.exec(stmt).first()
    if db_user_challenge:
        db_user_challenge.isRewarded = user_challenge_update.isRewarded
        db.add(db_user_challenge)
        db.commit()
        db.refresh(db_user_challenge)
        return create_response(True, "User Challenge Updated Successfully", db_user_challenge)
    return create_response(False, "User Challenge Not Found")

def delete_user_challenge(db: Session, user_challenge_id: int) -> dict:
    stmt = select(UserChallenge).where(UserChallenge.id == user_challenge_id)
    db_user_challenge = db.exec(stmt).first()
    if db_user_challenge:
        db.delete(db_user_challenge)
        db.commit()
        return create_response(True, "User Challenge Deleted Successfully")
    return create_response(False, "User Challenge Not Found")
