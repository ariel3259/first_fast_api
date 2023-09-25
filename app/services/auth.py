from app.repositories.users import UsersRepository
from app.db.models import Users
from app.utils.security import validate_password

class AuthService:
    users_repository: UsersRepository
    def __init__(self):
        self.users_repository = UsersRepository()

    def login(self, email: str, password: str) -> str | None:
        user: Users = self.users_repository.get_one_by(Users.email == email and Users.status is True)
        if user is None:
            return None
        result: bool = validate_password(password, user.password)
        if result is False:
            return None
        return user.email