from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from models.usermodel import User 
from database.connection import Base, engine
from router import user_router as ur
from router import admin_router as ar
from exception.password_exception import PasswordValidationException
from fastapi.exception_handlers import (
    http_exception_handler,
)

app = FastAPI()
Base.metadata.create_all(bind=engine)
app.include_router(ur.router, prefix='/api/v1')
app.include_router(ar.router, prefix='/api/v1')

@app.exception_handler(PasswordValidationException)
def password_validation_exception_handler(request: Request, exc: PasswordValidationException):
    return JSONResponse(
        status_code=400,
        content={"message": f"{exc.name} "},
    )