from fastapi import APIRouter
from .test import router as test_router

router = APIRouter(
    prefix="/api",
    tags=["api"],
)

router.include_router(test_router)
