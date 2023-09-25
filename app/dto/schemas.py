from pydantic import BaseModel
from typing import Generic, TypeVar, List

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

class UsersIn(BaseModel):
    name: str
    lastname: str
    email: str
    password: str

class LogInOut(BaseModel):
    access_token: str
    type: str

class TokenData(BaseModel):
    username: str