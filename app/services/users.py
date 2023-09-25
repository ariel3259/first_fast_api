from app.repositories.users import UsersRepository
from app.utils.security import get_password_hash
from app.dto.schemas import UsersIn
from app.db.models import Users

class UsersService:
    users_repository: UsersRepository
    def __init__(self):
        self.users_repository = UsersRepository()

    def create(self, user_dto: UsersIn) -> bool:
        hashed_password = get_password_hash(user_dto.password)
        user_email = self.users_repository.get_one_by(Users.email == user_dto.email)
        if user_email is not None:
            return False
        self.users_repository.persist(Users(
            name = user_dto.name,
            lastname = user_dto.lastname,
            email = user_dto.email,
            password = hashed_password,
            created_by = 'system',
            updated_by = 'system'
        ))
        return True
    
    def get_by_email(self, email: str) -> Users | None:
        return self.users_repository.get_one_by(Users.email == email)
        