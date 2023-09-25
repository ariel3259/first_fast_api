from app.repositories.repository import  Repository
from app.db.models import Users
from app.db.session import get_db
from sqlalchemy.orm import Session, Query
from sqlalchemy import ColumnExpressionArgument

class UsersRepository(Repository[Users]):
    def __init__(self):
        session: Session = get_db().__next__()
        query: Query[Users] = session.query(Users)
        default_criterion: ColumnExpressionArgument[bool] = Users.status is True
        super().__init__(session, query, default_criterion)
