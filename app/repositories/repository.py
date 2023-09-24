from sqlalchemy.orm import Session, Query
from sqlalchemy import ColumnExpressionArgument
from typing import Optional, TypeVar, Generic, List
from app.database.models import Base
from app.dto.schemas import Page

T = TypeVar('T', bound=Base)

class Repository(Generic[T]):
    session: Session
    query: Query[T]
    default_criterion: ColumnExpressionArgument[bool]

    def __init__(self, session: Session, query: Query[T], default_criterion: ColumnExpressionArgument[bool]):
        self.session = session
        self.query = query
        self.default_criterion = default_criterion
    
    #Get all records from db by an optional criterion, by default criterion is search if status is true
    def get_all(self, criterion: ColumnExpressionArgument[bool] | None = None) -> List[T]:
        if criterion is not None:
            return self.query.filter(criterion).all()
        else: return self.query.filter(self.default_criterion).all()

    #Get all records from db by an optional criterion, offset, and limit, the default criterion is search by status is true, the default offset is 0 and the default limit is 10
    def get_all_page(
        self,
        offset_op: int | None = None,
        limit_op: int | None = None,
        criterion: ColumnExpressionArgument[bool] | None = None) -> Page[T]:
        offset: int = 0
        limit: int = 10
        if offset_op is not None: offset = offset_op
        if limit_op is not None and limit_op > 0: limit = limit_op
        if criterion is not None:
            self.query.filter(criterion)
        else: self.query.filter(self.default_criterion)
        elements: List[T] = self.query.order_by('id').offset(offset).limit(limit).all()
        total_items = self.query.count()
        return Page[T](
            elements = elements,
            total_items = total_items
        )
    
    #Get One record by a criterion
    def get_one_by(self, criterion: ColumnExpressionArgument[bool]) -> Optional[T]:
        return self.query.filter(criterion).first()
    
    #Persist the record in the database, if doesn't exists,create a new one, else modify an existing record
    def persist(self, record: T) -> T:
        self.session.add(record)
        self.session.commit()
        self.session.refresh(record)
        return record

