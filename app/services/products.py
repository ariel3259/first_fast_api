from app.repositories.repository import Repository
from app.repositories.products import ProductsReposisotry
from app.database.models import Products
from app.dto.schemas import ProductBase, ProductOut, ProductUpdate, Page
from typing import Optional, List
from datetime import datetime

class ProductsService:
    products_repository: Repository[Products]
    def __init__(self):

        self.products_repository = ProductsReposisotry()
    
    def get_all(self, offset: int | None = None, limit: int | None = None) -> Page[ProductOut]:
        page: Page[Products] = self.products_repository.get_all_page(offset_op=offset, limit_op=limit)
        producs_out: List[ProductOut] = [ProductOut(
            id = x.id,
            name = x.name,
            price = x.price,
            stock = x.stock
        ) for x in page.elements]
        return Page[ProductOut](
            elements = producs_out,
            total_items = page.total_items
        )

    def get_by_id(self, id: int) -> ProductOut | None:
       product: Optional[Products] = self.products_repository.get_one_by(Products.id == id and Products.status is True)
       if product is None:
           return None
       return ProductOut(
            id = product.id,
            name = product.name,
            price = product.price,
            stock = product.stock
       )
    
    def create(self, product_base: ProductBase) -> ProductOut:
        product = self.products_repository.persist(
            Products(
                name = product_base.name,
                price = product_base.price,
                stock = product_base.stock,
                created_by = "system",
                updated_by = "system"
            )
        )
        return ProductOut(
            id = product.id,
            name = product.name,
            price = product.price,
            stock = product.stock
        )
    
    def update(self, product_update: ProductUpdate, id: int) -> ProductUpdate | None:
        product: Products = self.products_repository.get_by_id(id=id)
        if product is None:
            return None
        product.name = product_update.name is not None and product_update.name != product.name if product_update.name else product.name
        product.stock = product_update.stock is not None and product_update.stock != product.stock if product_update.stock else product.stock
        product.price = product_update.price is not None and product_update.price != product.price if product_update.price else product.price
        product.updated_at = datetime.today()
        product_updated = self.products_repository.persist(product)
        return ProductOut(
            id = product_updated.id,
            name = product_updated.name,
            price = product_updated.price,
            stock = product_updated.stock
        )

    def delete(self, id: int) -> bool:
        product: Products = self.products_repository.get_by_id(id=id)
        if product is None:
            return False
        product.status = False
        self.products_repository.persist(record=product)
