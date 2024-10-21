import hashlib
from sqlalchemy.orm import Session
from sqlmodel import select
from src.UserProfile.models import UserProfile
from .models import ReferralCode


def generate_referral_code(username: str, user_id: int) -> str:
    combined_str = f"{username}{user_id}"
    hash_object = hashlib.sha256(combined_str.encode())
    return hash_object.hexdigest()[:9].upper()


def create_referral_code(db: Session, user_id: int):
    # Fetch the user's information by their user ID
    user = db.exec(select(UserProfile).where(UserProfile.id == user_id)).first()

    if not user:
        raise ValueError("User not found")

    # Check if a referral code already exists for this user
    existing_referral_code = db.exec(select(ReferralCode).where(ReferralCode.user_id == user_id)).first()

    if existing_referral_code:
        return {
            "status": "true",
            "message": "Referral code already exists for this user",
            "data": existing_referral_code
        }

    # Generate the referral code
    referral_code_str = generate_referral_code(user.name, user.id)

    # Create a new ReferralCode entry
    new_referral_code = ReferralCode(
        user_id=user.id,
        referral_code=referral_code_str
    )

    db.add(new_referral_code)
    db.commit()
    db.refresh(new_referral_code)

    return {
        "status": "true",
        "message": "Referral code generated successfully",
        "data": new_referral_code
    }


def get_referral_code_by_user_id(db: Session, user_id: int):
    # Query to fetch the referral code associated with the given user_id
    referral_code = db.exec(select(ReferralCode).where(ReferralCode.user_id == user_id)).first()

    if not referral_code:
        raise ValueError("Referral code not found for this user ID")

    return {
            'status': 'true',
            'message': "Data Received Successfully",
            'data': referral_code
        }