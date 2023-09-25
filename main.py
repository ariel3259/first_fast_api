from fastapi import FastAPI, APIRouter
from app.routers.api import products, auth
from typing import List

app = FastAPI(
   title="Products Api"
)

routers: List[APIRouter] = [products.r, auth.r]
for router in routers:
    app.include_router(router)

@app.get("/")
def hi_word():
    return "hi word"