from configs.general import AVATARS_DIR
from configs.logger import init_logger
from dependencies.db import get_async_session
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from schemas.authors import AuthorSchema, CreateAuthorSchema, UpdateAuthorSchema
from services.authors import AuthorsService
from sqlalchemy.ext.asyncio import AsyncSession
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
        logger.error(f"Uploaind image error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error occurred during uploaind image",
        )


@router.post("/add-author", response_model=AuthorSchema)
async def add_author(
    author_data: CreateAuthorSchema, db: AsyncSession = Depends(get_async_session)
) -> AuthorSchema:
    try:
        return await AuthorsService.create_author(author_data, db)
    except Exception as e:
        logger.error(f"Creating author error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error duiring creating author",
        )


@router.patch("/update-author", response_model=AuthorSchema)
async def update_author(
    author_data: UpdateAuthorSchema, db: AsyncSession = Depends(get_async_session)
) -> AuthorSchema:
    try:
        return await AuthorsService.update_author(author_data, db)

    except Exception as e:
        logger.error(f"Updating author error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error duiring updating author",
        )
