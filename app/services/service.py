from app.services.products import ProductsService
from app.services.users import UsersService
from app.services.auth import AuthService
from fastapi import HTTPException


def get_service(service: str):
    match service:
        case "products":
            return ProductsService()
        case "users":
            return UsersService()
        case "auth":
            return AuthService()
        case _:
            raise HTTPException(503, "Service not available")