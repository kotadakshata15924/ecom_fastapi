from sqlalchemy import Column, UUID, String, TIMESTAMP, func
from database.connection import Base
from uuid import uuid4

class User(Base):
    __tablename__ = "user_table"
    id = Column(UUID(as_uuid=True), default=uuid4, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), unique=True, nullable=False)
    password = Column(String(400), nullable=False)
    role = Column(String(200), nullable=False, default='customer')
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())