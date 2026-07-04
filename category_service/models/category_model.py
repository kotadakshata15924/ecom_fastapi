from sqlalchemy import Column, UUID, String, TIMESTAMP, func
from database.connection import Base
from uuid import uuid4


class Category(Base):
    __tablename__ = "category_table"

    id = Column(UUID(as_uuid=True), default=uuid4, primary_key=True)
    name = Column(String(250), nullable=False, unique=True)
    description = Column(String(500), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
