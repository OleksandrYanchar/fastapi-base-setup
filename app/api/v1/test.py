from fastapi import APIRouter, File, HTTPException, UploadFile, status
from configs.general import AVATARS_DIR
from configs.logger import init_logger
from tasks.files import upload_picture

logger = init_logger(__file__)

router = APIRouter(prefix="/test", tags=["test"])


@router.get("/")
async def test():
    return {"message": "Hello World!"}


@router.post("/add-static")
async def update_photo(
    file: UploadFile = File(...),
):

    file_content = await file.read()
    filename = file.filename

    # Call the task with file content and filename
    task_result = upload_picture.delay(file_content, filename, AVATARS_DIR)
    file_url = task_result.get(timeout=10)

    try:
        return {"detail": "Image uploaded successfully.", "image": file_url}

    except Exception as e:
        logger.error(f"Verification error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error occurred during email verification",
        )
