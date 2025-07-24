from fastapi import APIRouter
from routes import users, auth, categories, material

router = APIRouter()

router.include_router(users.router)
router.include_router(auth.router)
router.include_router(categories.router)
router.include_router(material.router)