from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from configs.logger import init_logger
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

logger = init_logger(__file__)

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]) -> None:
        self._model = model

    async def create(self, db: AsyncSession, obj_in: CreateSchemaType) -> ModelType:
        try:
            obj_in_data = dict(obj_in)
            db_obj = self._model(**obj_in_data)
            db.add(db_obj)
            await db.commit()
            return db_obj
        except IntegrityError:
            raise Exception("Violations of unique constraints")
        except Exception as e:
            logger.error(f"Untracked error duiring creating: {e}", exc_info=True)

    async def get(self, session: AsyncSession, *args, **kwargs) -> Optional[ModelType]:
        try:
            result = await session.execute(
                select(self._model).filter(*args).filter_by(**kwargs)
            )
            return result.scalars().first()
        except Exception as e:
            logger.error(f"Untracked error duiring getting: {e}", exc_info=True)

    async def get_multi(
        self, db: AsyncSession, *args, offset: int = 0, limit: int = 100, **kwargs
    ) -> List[ModelType]:
        try:
            result = await db.execute(
                select(self._model)
                .filter(*args)
                .filter_by(**kwargs)
                .offset(offset)
                .limit(limit)
            )
            return result.scalars().all()
        except Exception as e:
            logger.error(f"Untracked error duiring getting multy: {e}", exc_info=True)

    async def update(
        self,
        db: AsyncSession,
        *,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]],
        db_obj: Optional[ModelType] = None,
        **kwargs,
    ) -> Optional[ModelType]:
        try:
            db_obj = db_obj or await self.get(db, **kwargs)
            if db_obj is not None:
                obj_data = db_obj.dict()
                if isinstance(obj_in, dict):
                    update_data = obj_in
                else:
                    update_data = obj_in.dict(exclude_unset=True)
                for field in obj_data:
                    if field in update_data:
                        setattr(db_obj, field, update_data[field])
                db.add(db_obj)
                await db.commit()
            return db_obj

        except IntegrityError:
            raise Exception("Violations of unique constraints")
        except Exception as e:
            logger.error(f"Untracked error during updating: {e}", exc_info=True)
            raise

    async def delete(
        self, db: AsyncSession, *args, db_obj: Optional[ModelType] = None, **kwargs
    ) -> ModelType:
        try:
            db_obj = db_obj or await self.get(db, *args, **kwargs)
            await db.delete(db_obj)
            await db.commit()
            return db_obj
        except Exception as e:
            logger.error(f"Untracked error duiring deleting: {e}", exc_info=True)
