from sqladmin import ModelView
from app.postgresql.models.users import Users

class UsersModelView(ModelView, model=Users):
    
    column_list = [Users.id, Users.username, Users.email, Users.first_name, Users.last_name]
    column_searchable_list = [Users.id, Users.username, Users.email, Users.last_name]
    
    column_default_sort =  "username"

