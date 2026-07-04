from sqlalchemy import Column,UUID,String,TIMESTAMP,func,Text,Numeric,Integer
from database.connection import Base
import uuid

class Product(Base):
    __tablename__='product_table'
    id = Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    name = Column(String(250),nullable=False,unique=True)
    description = Column(Text, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    image_url = Column(String(250), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),server_default=func.now())
    category_id = Column(UUID(as_uuid=True), nullable=False)