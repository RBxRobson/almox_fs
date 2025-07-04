from fastapi import FastAPI
from routes import users

app = FastAPI()

# Rota users, criação, listagem e detalhes do usuário ativo (Protegida)
app.include_router(users.router)
