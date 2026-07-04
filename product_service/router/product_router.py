from uuid import UUID
from typing import Optional
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from database.connection import Session
from database.dependencies import get_db
from models.product_model import Product
from schema.product_schema import (
    ProductCreateSchema,
    ProductUpdateSchema,
    ProductResponseSchema,
)
from core.authentication import get_current_user, get_admin_user
from core.category_client import verify_category_exists
from exception.product_exception import ProductNotFoundException

router = APIRouter()


@router.post('/product', status_code=status.HTTP_201_CREATED)
def create_product(
    request: ProductCreateSchema,
    db: Session = Depends(get_db),
    admin: dict = Depends(get_admin_user(('Admin', 'admin'))),
):
    verify_category_exists(request.category_id)

    product = Product(
        name=request.name,
        description=request.description,
        price=request.price,
        stock=request.stock,
        category_id=request.category_id,
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return JSONResponse(
        {"message": "product created successfully", "id": str(product.id)},
        status_code=status.HTTP_201_CREATED,
    )


@router.get('/product', response_model=list[ProductResponseSchema])
def list_products(category_id: Optional[UUID] = None, db: Session = Depends(get_db)):
    query = db.query(Product)
    if category_id:
        query = query.filter(Product.category_id == category_id)
    return query.all()


@router.get('/product/{product_id}', response_model=ProductResponseSchema)
def get_product(product_id: UUID, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise ProductNotFoundException("product not found")
    return product


@router.put('/product/{product_id}')
def update_product(
    product_id: UUID,
    request: ProductUpdateSchema,
    db: Session = Depends(get_db),
    admin: dict = Depends(get_admin_user(('Admin', 'admin'))),
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise ProductNotFoundException("product not found")

    if request.category_id is not None:
        verify_category_exists(request.category_id)
        product.category_id = request.category_id
    if request.name is not None:
        product.name = request.name
    if request.description is not None:
        product.description = request.description
    if request.price is not None:
        product.price = request.price
    if request.stock is not None:
        product.stock = request.stock

    db.commit()
    db.refresh(product)
    return {"message": "product updated successfully"}


@router.delete('/product/{product_id}')
def delete_product(
    product_id: UUID,
    db: Session = Depends(get_db),
    admin: dict = Depends(get_admin_user(('Admin', 'admin'))),
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise ProductNotFoundException("product not found")

    db.delete(product)
    db.commit()
    return {"message": "product deleted successfully"}
