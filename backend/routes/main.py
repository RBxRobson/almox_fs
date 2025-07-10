from fastapi import APIRouter
from routes import users, auth

router = APIRouter()

router.include_router(users.router)
router.include_router(auth.router)