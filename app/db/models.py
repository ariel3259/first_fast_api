from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer, Boolean, Float, DateTime
from datetime import datetime

class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.today)
    created_by: Mapped[str] = mapped_column(String(50))
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.today)
    updated_by: Mapped[str] = mapped_column(String(50))
    status: Mapped[bool] = mapped_column(Boolean, default=True)

class Products(Base):
    __tablename__ = "products"
    price: Mapped[float] = mapped_column(Float)
    name: Mapped[str] = mapped_column(String)
    stock: Mapped[int] = mapped_column(Integer)


class Users(Base):
    __tablename__ = "users"
    name: Mapped[str] = mapped_column(String(50))
    lastname: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))

