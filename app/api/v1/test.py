from fastapi import APIRouter

from tasks.test import test_celery

router = APIRouter(prefix="/test", tags=["test"])

@router.get("/")
async def test():
    return {"message": "Hello World!"} 


@router.get("/celery")
async def test():
    message = test_celery.delay()
    return {"task_id": message.id, "task_status": message.status}