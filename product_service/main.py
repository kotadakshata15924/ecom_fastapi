from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from database.connection import Base, engine
from models.product_model import Product
from router import product_router as pr
from exception.product_exception import (
    ProductNotFoundException,
    InvalidCategoryException,
    CategoryServiceUnavailableException,
)

app = FastAPI(title="Product Service")
Base.metadata.create_all(bind=engine)

app.include_router(pr.router, prefix='/api/v1')


@app.exception_handler(ProductNotFoundException)
def product_not_found_handler(request: Request, exc: ProductNotFoundException):
    return JSONResponse(status_code=404, content={"message": exc.name})


@app.exception_handler(InvalidCategoryException)
def invalid_category_handler(request: Request, exc: InvalidCategoryException):
    return JSONResponse(status_code=400, content={"message": exc.name})


@app.exception_handler(CategoryServiceUnavailableException)
def category_service_down_handler(request: Request, exc: CategoryServiceUnavailableException):
    return JSONResponse(status_code=503, content={"message": exc.name})
