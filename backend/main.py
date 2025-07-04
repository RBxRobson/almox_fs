from fastapi import FastAPI
from routes.main import router as api_router

app = FastAPI(title="Almoxarifado API")

app.include_router(api_router, prefix="/api")
