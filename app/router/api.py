from fastapi import APIRouter
from endpoint import user , login

api_router = APIRouter()

api_router.include_router(user.router, tags=["Users"])
api_router.include_router(login.router, tags=["Login"])