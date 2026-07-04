from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from schema.user_schema import UserCreateSchema, UserLoginSchema, RefreshToken
from database.connection import Session
from database.dependencies import get_db
from core.password_val import hash_password, verify_password
from models.usermodel import User
from fastapi import status
from core.gen_jwt import generate_access, generate_refresh, decode_refresh
from core.authentication import get_current_user
from jose import jwt

router = APIRouter()

@router.post('/user/signup')
def create_user(request: UserCreateSchema, db:Session=Depends(get_db)):
    hp = hash_password(password=request.password)
    user_data = User(
        name =  request.name,
        email = request.email,
        password = hp
    )
    db.add(user_data)
    db.commit()
    return JSONResponse(
        {'message':"user created ssuccessfully"},
        status_code=status.HTTP_201_CREATED
    )

@router.post('/user/login')
def login(request: UserLoginSchema, db: Session=Depends(get_db)):
    email =  request.email
    db_data = db.query(User).filter(User.email==email).first()
    if not db_data:
        raise HTTPException(404, detail={'message':'user with email not exist'})
    db_pw = db_data.password
    req_pw = request.password
    if not verify_password(req_pw, db_pw):
        raise HTTPException(400, detail={'message':'incorrect password'})
    access_token = generate_access(id=db_data.id, name=db_data.name, email=db_data.email, role=db_data.role)
    refresh_token = generate_refresh(id=db_data.id, name=db_data.name, email=db_data.email, role=db_data.role)
    return {
        'access_token': access_token,
        'refresh_token': refresh_token
    }

@router.get('/user/profile')
def showprofile(user: dict= Depends(get_current_user)):
    return user

@router.post('/user/refresh')
def access_token_generation(token: RefreshToken):
    access_token = decode_refresh(token.refresh_token)
    return {'access_token': access_token}