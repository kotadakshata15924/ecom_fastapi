from fastapi import APIRouter, Depends
from core.authentication import get_admin_user 

router = APIRouter()

@router.get('/admin/profile')
def adminprofile(user: dict=Depends(get_admin_user(('Admin', 'admin')))):
    return user