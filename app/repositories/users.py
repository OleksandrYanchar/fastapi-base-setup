from app.models.users import Users
from app.repositories.base import BaseRepository
from app.schemas.users import UpdateUserDataSchema, UserCreateInSchema

UsersRepository = BaseRepository[Users, UserCreateInSchema, UpdateUserDataSchema]


users_repository = UsersRepository(Users)
