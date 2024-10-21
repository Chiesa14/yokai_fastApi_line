from fastapi.routing import APIRouter

from src.UserProfile.views import router as user_profile_router
from src.Stories.views import router as stories_router
from src.Chapter.views import router as chapter_router
from src.Activity.views import router as activity_router
from src.ActivityDetails.views import router as activity_details_router
from src.Character.views import router as character_router
from src.ChapterWiseUser.views import router as chapter_wise_user_router
from src.CharacterChat.views import router as character_chat_router
from src.UserCharacter.views import router as user_character_router
from src.CharacterSummary.views import router as character_summary_router
from src.MoodTracker.views import router as mood_tracker_router
from src.Todo.views import router as todo_router
from src.Referal.views import router as referral_router
from src.ReferalInvitation.views import router as referral_invitation_router
from src.UserLogs.views import router as user_logs_router
from src.Challenge.views import router as challenge_router
from src.Compliment.views import router as compliment_router
from src.Quiz.views import router as quiz_router
# from src.Badges.views import router as badges_router
from src.Devices.views import router as devices_router

api_router = APIRouter()

api_router.include_router(user_profile_router, prefix="/user_profile", tags=["UserProfile"])

api_router.include_router(stories_router, prefix="/stories", tags=["Stories"])

api_router.include_router(chapter_router, prefix="/chapter", tags=["Chapter"])

api_router.include_router(activity_router, prefix="/activity", tags=["Activity"])

api_router.include_router(activity_details_router, prefix="/activity_details", tags=["ActivityDetails"])

api_router.include_router(character_router, prefix="/character", tags=["Character"])

api_router.include_router(chapter_wise_user_router, prefix="/chapter_wise_user", tags=["ChapterWiseUser"])

api_router.include_router(character_chat_router, prefix="/character_chat", tags=["CharacterChat"])

api_router.include_router(user_character_router, prefix="/user_character", tags=["UserCharacter"])
api_router.include_router(character_summary_router, prefix="/character_summary", tags=["CharacterSummary"])
api_router.include_router(mood_tracker_router, prefix="/mood_tracker", tags=["MoodTrack"])

api_router.include_router(todo_router,prefix='/todo',tags=["ToDo"])

api_router.include_router(referral_router,prefix='/referral',tags=["Referral"])
api_router.include_router(referral_invitation_router,prefix='/referral',tags=["ReferralInvitation"])
api_router.include_router(user_logs_router,prefix='/logs',tags=["Referral"])

api_router.include_router(challenge_router,prefix='/challenge',tags=["Challenge"])
api_router.include_router(compliment_router,prefix='/compliment',tags=["Compliment"])

# api_router.include_router(badges_router,prefix='/badges',tags=["Badges"])
api_router.include_router(devices_router,prefix='/devices',tags=["Devices"])

api_router.include_router(quiz_router,prefix='/quiz',tags=["Quiz"])