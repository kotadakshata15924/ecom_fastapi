from pydantic import BaseModel, field_validator
from typing import Optional
from uuid import UUID
from datetime import datetime


class CategoryCreateSchema(BaseModel):
    name: str
    description:str| None

    @field_validator('name')
    @classmethod
    def name_validator(cls, value):
        if len(value.strip()) < 2:
            raise ValueError("category name must be at least 2 characters long")
        return value.strip()



class CategoryResponseSchema(BaseModel):
    id: UUID
    name: str
    description:str| None
    created_at: datetime

    class Config:
        from_attributes = True
