from dotenv import load_dotenv
import os
from jose import jwt
from datetime import timedelta, datetime, UTC
from fastapi import HTTPException, status

load_dotenv()

secret_key = os.getenv('SECRET_KEY')
access_token_expire = os.getenv('ACCESS_TOKEN_EXPIRE')
refresh_token_expire = os.getenv('REFRESH_TOKEN_EXPIRE')
algorithm = os.getenv('ALGORITHM')

def generate_access(**kwargs):
    data = kwargs.copy()
    expire = datetime.now(UTC) + timedelta(minutes=int(access_token_expire))
    access_token = jwt.encode({
        'id': str(data['id']),
        'name': data['name'],
        'email': data['email'],
        'role': data['role'],
        'exp': expire
    },secret_key, algorithm)
    return access_token

def decode_refresh(token: str):
    payload = jwt.decode(
        token,
        secret_key,
        algorithm
    )
    expire_time = payload['exp']
    current_time = datetime.now(UTC).timestamp()
    if int(current_time) > expire_time:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='refresh token expired'
        )
    return generate_access(id=payload['id'],
                           name=payload['name'],
                           email=payload['email'],
                           role=payload['role'],
                           )

def generate_refresh(**kwargs):
    data = kwargs.copy()
    expire = datetime.now(UTC) + timedelta(minutes=refresh_token_expire)
    payload = {
        "id": str(data["id"]),
        "name": data["name"],
        "email": data["email"],
        "role": data["role"],
        "exp": expire,
    }
    refresh_token = jwt.encode(payload,secret_key,algorithm=algorithm)
    return refresh_token



