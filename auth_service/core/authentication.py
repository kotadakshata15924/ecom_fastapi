from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from jose import jwt
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta, UTC

oauthschema = OAuth2PasswordBearer(tokenUrl='/login')
secret_key = os.getenv("SECRET_KEY")
algorithm = os.getenv('ALGORITHM')

def get_current_user(access_token: str=Depends(oauthschema)):
    try:
        payload = jwt.decode(
        access_token, 
        secret_key,
        algorithm
        )
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"message":"invalid access token"}
        )
    expire_time = payload['exp']
    current_time = datetime.now(UTC).timestamp()
    if int(current_time) > expire_time:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={'message': 'token got expired'}
        )
    return payload



def get_current_user(refresh_token: str=Depends(oauthschema)):
    try:
        payload = jwt.decode(
        refresh_token, 
        secret_key,
        algorithm
        )
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"message":"invalid refresh token"}
        )
    expire_time = payload['exp']
    current_time = datetime.now(UTC).timestamp()
    if int(current_time) > expire_time:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={'message': 'token got expired'}
        )
    return payload

def get_admin_user(role):
    def get_user(user: dict=Depends(get_current_user)):
        if user['role'] in role:
            return user
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="you don't have access to this endpoint")
    return get_user