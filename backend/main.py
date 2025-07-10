from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from routes.main import router as api_router

app = FastAPI(title="Almoxarifado API")

@app.get("/", response_class=HTMLResponse)
def root():
    return """
    <html>
        <head><title>API Almoxarifado</title></head>
        <body style="font-family: sans-serif; text-align: center; padding: 2rem;">
            <h1>✅ API Almoxarifado Rodando</h1>
            <p>Acesse <a href="/docs">/docs</a> para visualizar a documentação.</p>
        </body>
    </html>
    """

app.include_router(api_router)
