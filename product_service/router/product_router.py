from fastapi import APIRouter, Depends, HTTPException,Form,File,UploadFile 
from sqlalchemy.orm import Session
from decimal import Decimal
from models.product_model import Product
from schema.product_schema import ProductCreateSchema,ProductResponseSchema
from database.dependencies import get_db
from fastapi.responses import JSONResponse
import uuid
import httpx
from core.authentication import get_current_user, get_admin_user

router = APIRouter()

CATEGORY_SERVICE_URL = "http://localhost:8001"

@router.post("/products", response_model=ProductResponseSchema,)
async def create_product(
    name: str = Form(...),
    description: str = Form(...),
    price: Decimal = Form(...),
    image: UploadFile = File(...),
    category_name: str = Form(...),
    db: Session = Depends(get_db),
    admin: dict = Depends(get_admin_user(('Admin', 'admin')))
    ):
    
    image_data = await image.read()

    filename = f"media/{image.filename}"

    with open(filename, "wb") as file:
        file.write(image_data)

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"http://category-service:8001/categories/name/{category_name}"
        )

    if response.status_code != 200:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    category = response.json()

    product = Product(
        id=uuid.uuid4(),
        name=name,
        description=description,
        price=price,
        image_url=filename,
        category_id=category["id"]
    )

    db.add(product)
    db.commit()
    db.refresh(product)

    return product
@router.get("/products", response_model=list[ProductResponseSchema])
def get_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return products
@router.get("/products/{product_id}",response_model=ProductResponseSchema)
def get_product(product_id:uuid.UUID,db:Session=Depends(get_db)):
    product=db.query(Product).filter(Product.id==product_id).first()
    if not product:
        raise HTTPException(status_code=404,detail="Product not found")
    # return JSONResponse({'id': product.id, 'name': product.name, 'description': product.description, 'price': product.price})
    return product