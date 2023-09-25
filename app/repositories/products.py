from app.db.models import Products
from app.repositories.repository import Repository
from app.db.session import get_db
from sqlalchemy.orm import Query
from sqlalchemy import ColumnExpressionArgument

class ProductsReposisotry(Repository[Products]):
    def __init__(self):
        session = get_db().__next__()
        query: Query[Products] = session.query(Products)
        default_criterion: ColumnExpressionArgument[bool] = Products.status == True
        super().__init__(session, query, default_criterion)