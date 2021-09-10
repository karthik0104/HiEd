from entity.user import User
from service.user import UserService

user = User(id=1, name='karthik')

user_service = UserService()
user_service.persist_user_location(user, '34.45', '45.56')

