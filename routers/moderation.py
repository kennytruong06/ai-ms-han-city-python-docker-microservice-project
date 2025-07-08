from fastapi import APIRouter
from helpers.cleanup import cleanup_file_temp
from schemas.moderation import ModerationRequest, ModerationResponse
from services.moderation_picture_service import analyze_pictures
from services.moderation_text_service import analyze_texts
from services.moderation_video_service import analyze_videos

router = APIRouter(prefix="/moderation", tags=["Moderation"])

@router.post("/check", response_model=ModerationResponse)
async def check_content(payload: ModerationRequest):
    all_results = [
        analyze_texts(payload.content),
        analyze_pictures(payload.pictures),
        analyze_videos(payload.videos)
    ]
    cleanup_file_temp()

    return ModerationResponse(data=all_results)
