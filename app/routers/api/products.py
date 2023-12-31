from fastapi import APIRouter, Response, Depends, HTTPException
from app.dto.schemas import ProductBase, ProductOut, ProductUpdate, Page
from app.services.service import get_service
from app.utils.security import get_current_active_user
from app.db.models import Users
from typing import List

r = APIRouter(
    tags=["products"],
    prefix="/api/products",
    dependencies=[Depends(get_current_active_user)]
)

products_service = lambda : get_service("products")

@r.get('')
def get_all(res: Response, service = Depends(products_service), offset: int | None = None, limit: int | None = None ) -> List[ProductOut]:
    page: Page[ProductOut] = service.get_all(offset=offset, limit=limit)
    res.headers.append("x-total-count", "{}".format(page.total_items))
    return page.elements


@r.post('')
def save(product_base: ProductBase, service = Depends(products_service), current_user: Users = Depends(get_current_active_user)) -> ProductOut:
    product_out: ProductOut = service.create(product_base, current_user.email)
    return product_out

@r.get('/{id}')
def get_by_id(id: int, res: Response, service = Depends(products_service)) -> ProductOut | None:
    product_out: ProductOut | None = service.get_by_id(id);
    if product_out is None:
        res.status_code = 204
        return
    return product_out

@r.put('/{id}')
def update(id: int, product_update: ProductUpdate, service = Depends(products_service), current_user: Users = Depends(get_current_active_user)):
    product_out: ProductOut | None = service.update(id=id, product_update=product_update, username=current_user.email)
    if product_out is None:
        raise HTTPException(400, "The product does not exits")
    return product_out

@r.delete("/{id}")
def delete(id: int, res: Response, service = Depends(products_service)):
    result = service.delete(id)
    if result is False:
        raise HTTPException(400, "The product does not exits")
    res.status_code = 204
    return