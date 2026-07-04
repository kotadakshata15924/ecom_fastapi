import os
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError

# IMPORTANT: this must be the exact same SECRET_KEY / ALGORITHM used by auth_service
# to sign the access token, otherwise verification here will always fail.
# Set it as an environment variable so all services share the same value:
#   export JWT_SECRET_KEY="same-secret-as-auth-service"
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "change-me-shared-secret")
ALGORITHM = "HS256"

bearer_scheme = HTTPBearer()


def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"message": "invalid or expired token"},
        )


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)) -> dict:
    payload = decode_access_token(credentials.credentials)
    return payload


def get_admin_user(allowed_roles: tuple = ("Admin", "admin")):
    def _verify_admin(user: dict = Depends(get_current_user)) -> dict:
        if user.get("role") not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={"message": "you do not have permission to perform this action"},
            )
        return user
    return _verify_admin
