from app.services.products import ProductsService
from fastapi import HTTPException

def get_service(service: str):
    match service:
        case "products":
            return ProductsService()
        case _:
            raise HTTPException(503, "Service not available")