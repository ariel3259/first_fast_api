from fastapi import FastAPI, APIRouter
from app.routers.api import products
from typing import List

app = FastAPI()

routers: List[APIRouter] = [products.r]
for router in routers:
    app.include_router(router)

@app.get("/")
def hi_word():
    return "hi word"