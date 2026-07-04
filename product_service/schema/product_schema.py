from pydantic import BaseModel, field_validator
from typing import Optional
from uuid import UUID
from datetime import datetime


class ProductCreateSchema(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    stock: int = 0
    category_id: UUID

    @field_validator('price')
    @classmethod
    def price_validator(cls, value):
        if value <= 0:
            raise ValueError("price must be greater than 0")
        return value

    @field_validator('stock')
    @classmethod
    def stock_validator(cls, value):
        if value < 0:
            raise ValueError("stock cannot be negative")
        return value


class ProductUpdateSchema(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None
    category_id: Optional[UUID] = None


class ProductResponseSchema(BaseModel):
    id: UUID
    name: str
    description: Optional[str] = None
    price: float
    stock: int
    category_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True
