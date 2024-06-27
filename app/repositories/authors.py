from models.authors import Author
from repositories.base import BaseRepository
from schemas.authors import CreateAuthorSchema, UpdateAuthorSchema

AuthorRepository = BaseRepository[Author, CreateAuthorSchema, UpdateAuthorSchema]


author_repository = AuthorRepository(Author)
