from sqlalchemy.orm import Session
from sqlmodel import select
from src.UserProfile.models import UserProfile
from src.Referal.models import ReferralCode
from .model import Invitation

def handle_user_signup_with_referral(db: Session, referred_user_id: int, referral_code: str):
    # Fetch the invitation details using the referral code
    referral = db.exec(select(ReferralCode).where(ReferralCode.referral_code == referral_code)).first()

    if not referral:
        raise ValueError("Invalid referral code")

    invitation = db.exec(select(Invitation).where(Invitation.referral_code == referral_code)).first()

    if not invitation:
        new_invitation = Invitation(
            user_id=referral.user_id,
            referral_code=referral_code,
            invite_count=1
        )
        db.add(new_invitation)
    else:
        invitation.invite_count += 1

    db.commit()

    return {
        "status": "true",
        "message": "User signed up with referral and invite count updated",
        "data": invitation if invitation else new_invitation
    }


def get_invitation_by_referral_code(db: Session, referral_code: str):
    invitation = db.exec(select(Invitation).where(Invitation.referral_code == referral_code)).first()

    if not invitation:
        raise ValueError("No invitations found for this referral code")

    return {
        "status": "true",
        "message": "Invitation data fetched successfully",
        "data": invitation
    }