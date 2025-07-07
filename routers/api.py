from fastapi import APIRouter
from routers import moderation

router = APIRouter(prefix="/api", tags=["API"])
router.include_router(moderation.router)
