from pydantic import BaseModel
from decimal import Decimal
from uuid import UUID


class ProductCreateSchema(BaseModel):
    name: str
    description: str|None=None
    price: Decimal
    image: str

class ProductResponseSchema(BaseModel):
    id: UUID
    name: str
    description: str|None=None
    price: Decimal
    image: str

    model_config = {
        "from_attributes": True
    }