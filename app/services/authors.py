from configs.logger import init_logger
from repositories.authors import author_repository
from schemas.authors import AuthorSchema, CreateAuthorSchema, UpdateAuthorSchema
from sqlalchemy.ext.asyncio import AsyncSession

logger = init_logger(__file__)


class AuthorsService:

    @staticmethod
    async def create_author(
        author_data: CreateAuthorSchema, db: AsyncSession
    ) -> AuthorSchema:
        try:
            new_author = await author_repository.create(db, obj_in=author_data)
            return AuthorSchema(**new_author.dict())
        except Exception as e:
            logger.error(f"Error during creating author:  {e}", exc_info=True)
            raise Exception("Error during creating author")

    @staticmethod
    async def update_author(
        author_data: UpdateAuthorSchema, db: AsyncSession
    ) -> AuthorSchema:
        try:
            author_obj = await author_repository.get(db, id=author_data.id)

            updated_author = {"name": author_data.name}
            new_author = await author_repository.update(
                db, db_obj=author_obj, obj_in=updated_author
            )
            return AuthorSchema(**new_author.dict())
        except Exception as e:
            logger.error(f"Error during updating author: {e}", exc_info=True)
            raise Exception("Error during updating author")
