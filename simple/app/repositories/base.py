# Import necessary libraries and modules
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.ext.asyncio import AsyncSession

from app.configs.logger import init_logger

logger = init_logger(__file__)

# Define type variables for the generic repository
ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


# Define a base repository class using generics
class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    Base repository class
    parameters:
    model: The SQLAlchemy model class
    crateSchema: pydantic schema used for creating this model object
    """

    def __init__(self, model: Type[ModelType]) -> None:
        # Initialize with the model class
        self._model = model

    # Asynchronous method to create a new object in the database
    async def create(self, db: AsyncSession, obj_in: CreateSchemaType) -> ModelType:
        # Convert Pydantic model to dictionary
        obj_in_data = dict(obj_in)
        # Create an instance of the SQLAlchemy model
        db_obj = self._model(**obj_in_data)
        # Add the object to the session and commit
        db.add(db_obj)
        await db.commit()
        # Refresh the session to get the latest state of the object
        try:
            await db.refresh(db_obj)
        except InvalidRequestError as e:
            logger.error(f"Could not refresh instance '{db_obj}': {e}")
        return db_obj

    # Asynchronous method to get a single object based on filters
    async def get(self, session: AsyncSession, *args, **kwargs) -> Optional[ModelType]:
        result = await session.execute(
            select(self._model).filter(*args).filter_by(**kwargs)
        )
        # Return the first result
        return result.scalars().first()

    # Asynchronous method to get multiple objects based on filters, with pagination
    async def get_multi(
        self, db: AsyncSession, *args, offset: int = 0, limit: int = 100, **kwargs
    ) -> List[ModelType]:
        result = await db.execute(
            select(self._model)
            .filter(*args)
            .filter_by(**kwargs)
            .offset(offset)
            .limit(limit)
        )
        # Return all results
        return result.scalars().all()

    # Asynchronous method to delete an object based on filters or a provided object
    async def delete(
        self, db: AsyncSession, *args, db_obj: Optional[ModelType] = None, **kwargs
    ) -> ModelType:
        # Get the object if not provided
        db_obj = db_obj or await self.get(db, *args, **kwargs)
        # Delete the object from the session and commit
        await db.delete(db_obj)
        await db.commit()
        return db_obj

    async def update(
        self,
        db: AsyncSession,
        *,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]],
        db_obj: Optional[ModelType] = None,
        **kwargs,
    ) -> Optional[ModelType]:
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
