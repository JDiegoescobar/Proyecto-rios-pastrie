from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import usuario_router

app = FastAPI(
    title="Ríos Pastries API",
    description="Sistema de gestión de pedidos y eventos",
    version="1.0.0"
)

# ✅ CONFIGURACIÓN CORS (MUY IMPORTANTE)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8080", "http://localhost:8080", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(usuario_router.router)

@app.get("/")
def root():
    return {"mensaje": "Bienvenido a la API de Ríos Pastries"}