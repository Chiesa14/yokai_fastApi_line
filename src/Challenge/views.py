from fastapi import FastAPI, Depends, HTTPException, APIRouter
from sqlmodel import Session
from .model import ChallengeCreate, UserChallengeCreate
from src.Challenge.service import (
    create_challenge,
    get_challenge,
    get_challenges,
    update_challenge,
    delete_challenge,
    create_user_challenge,
    get_user_challenge,
    get_user_challenges,
    update_user_challenge,
    delete_user_challenge,
)
from src.database import get_db

router = APIRouter()

# Challenge Endpoints
@router.post("/create/")
def create_challenge_endpoint(challenge: ChallengeCreate, db: Session = Depends(get_db)):
    return create_challenge(db, challenge)

@router.get("/challenges/{challenge_id}")
def read_challenge(challenge_id: int, db: Session = Depends(get_db)):
    challenge = get_challenge(db, challenge_id)
    if challenge is None:
        raise HTTPException(status_code=404, detail="Challenge not found")
    return challenge

@router.get("/challenges")
def read_challenges(db: Session = Depends(get_db)):
    return get_challenges(db)

@router.put("/challenges/{challenge_id}")
def update_challenge_endpoint(challenge_id: int, challenge_update: ChallengeCreate, db: Session = Depends(get_db)):
    updated_challenge = update_challenge(db, challenge_id, challenge_update)
    if updated_challenge is None:
        raise HTTPException(status_code=404, detail="Challenge not found")
    return updated_challenge

@router.delete("/challenges/{challenge_id}")
def delete_challenge_endpoint(challenge_id: int, db: Session = Depends(get_db)):
    success = delete_challenge(db, challenge_id)
    if not success:
        raise HTTPException(status_code=404, detail="Challenge not found")
    return {"detail": "Challenge deleted"}

# UserChallenge Endpoints
@router.post("/user-challenges/")
def create_user_challenge_endpoint(user_challenge: UserChallengeCreate, db: Session = Depends(get_db)):
    return create_user_challenge(db, user_challenge)

@router.get("/user-challenges/{user_challenge_id}")
def read_user_challenge(user_challenge_id: int, db: Session = Depends(get_db)):
    user_challenge = get_user_challenge(db, user_challenge_id)
    if user_challenge is None:
        raise HTTPException(status_code=404, detail="UserChallenge not found")
    return user_challenge

@router.get("/user-challenges/user/{user_id}")
def read_user_challenges(user_id: int, db: Session = Depends(get_db)):
    return get_user_challenges(db, user_id)

@router.put("/user-challenges/{user_challenge_id}")
def update_user_challenge_endpoint(user_challenge_id: int, user_challenge_update: UserChallengeCreate, db: Session = Depends(get_db)):
    updated_user_challenge = update_user_challenge(db, user_challenge_id, user_challenge_update)
    if updated_user_challenge is None:
        raise HTTPException(status_code=404, detail="UserChallenge not found")
    return updated_user_challenge

@router.delete("/user-challenges/{user_challenge_id}")
def delete_user_challenge_endpoint(user_challenge_id: int, db: Session = Depends(get_db)):
    success = delete_user_challenge(db, user_challenge_id)
    if not success:
        raise HTTPException(status_code=404, detail="UserChallenge not found")
    return {"detail": "UserChallenge deleted"}
