from fastapi import APIRouter

from app.api.auth import router as auth_router
from app.api.profiles import router as profiles_router

router = APIRouter(
    prefix="/users",
)

router.include_router(auth_router)
router.include_router(profiles_router)
