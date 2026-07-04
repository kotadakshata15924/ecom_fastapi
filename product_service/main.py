from fastapi import FastAPI
from router import product_router as pr
from database.connection import Base, engine

app = FastAPI()
Base.metadata.create_all(bind=engine)
app.include_router(pr.router, prefix='/api/v1')