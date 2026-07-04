from sqlalchemy import Column, UUID, String, Integer, Float, TIMESTAMP, func
from database.connection import Base
from uuid import uuid4


class Product(Base):
    __tablename__ = "product_table"

    id = Column(UUID(as_uuid=True), default=uuid4, primary_key=True)
    name = Column(String(250), nullable=False)
    description = Column(String(500), nullable=True)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False, default=0)
    # no FK constraint on purpose: category lives in a different service/database.
    # we only store the reference id and validate it via an HTTP call.
    category_id = Column(UUID(as_uuid=True), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
