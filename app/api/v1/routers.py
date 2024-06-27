from fastapi import APIRouter

from .test import router as test_router

router = APIRouter(
    prefix="/v1",
)

router.include_router(test_router)
