from pydantic import BaseModel
from typing import Optional, Generic, TypeVar, List
from app.database.models import Products

T = TypeVar('T')

class Page(Generic[T]):
    elements: List[T]
    total_items: int
    def __init__(self, elements: List[T], total_items: int):
        self.elements = elements
        self.total_items = total_items

class ProductBase(BaseModel):
    name: str
    price: float
    stock: int

class ProductOut(ProductBase):
    id: int
    pass

class ProductUpdate(BaseModel):
    name: str | None = None
    price: float | None = None
    stock: int | None = None
