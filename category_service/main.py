from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from database.connection import Base, engine
from models.category_model import Category
from router import category_router as cr
from exception.category_exception import CategoryNotFoundException, CategoryAlreadyExistsException

app = FastAPI(title="Category Service")
Base.metadata.create_all(bind=engine)

app.include_router(cr.router, prefix='/api/v1')


@app.exception_handler(CategoryNotFoundException)
def category_not_found_handler(request: Request, exc: CategoryNotFoundException):
    return JSONResponse(status_code=404, content={"message": exc.name})


@app.exception_handler(CategoryAlreadyExistsException)
def category_exists_handler(request: Request, exc: CategoryAlreadyExistsException):
    return JSONResponse(status_code=400, content={"message": exc.name})
