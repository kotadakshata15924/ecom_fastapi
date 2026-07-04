from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from database.connection import Session
from database.dependencies import get_db
from models.category_model import Category
from schema.category_schema import (
    CategoryCreateSchema,
    CategoryResponseSchema,
)
from core.authentication import get_current_user, get_admin_user
from exception.category_exception import CategoryNotFoundException, CategoryAlreadyExistsException

router = APIRouter()


@router.post('/category', status_code=status.HTTP_201_CREATED)
def create_category(
    request: CategoryCreateSchema,
    db: Session = Depends(get_db),
    admin: dict = Depends(get_admin_user(('Admin', 'admin'))),
):
    existing = db.query(Category).filter(Category.name == request.name).first()
    if existing:
        raise CategoryAlreadyExistsException(f"category '{request.name}' already exists")

    category = Category(name=request.name, description=request.description)
    db.add(category)
    db.commit()
    db.refresh(category)
    return JSONResponse(
        {"message": "category created successfully", "id": str(category.id)},
        status_code=status.HTTP_201_CREATED,
    )


@router.get('/category', response_model=list[CategoryResponseSchema])
def list_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()


@router.get('/category/{category_id}', response_model=CategoryResponseSchema)
def get_category(category_id: UUID, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise CategoryNotFoundException("category not found")
    return category


