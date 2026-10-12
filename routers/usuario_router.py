# routers/usuario_router.py
from fastapi import APIRouter, HTTPException, status
from models.usuario import UsuarioLogin, UsuarioRegistro, TokenResponse
from services.database import get_db  # Ajusta según donde tengas database.py
import bcrypt
import jwt
import os
from datetime import datetime, timedelta

router = APIRouter(prefix="/api/usuarios", tags=["Usuarios"])

@router.post("/login", response_model=TokenResponse)
def login(data: UsuarioLogin):
    # 1. Conectar a la base de datos
    db = get_db()
    if not db:
        raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")

    cursor = db.cursor(dictionary=True)
    
    # 2. Buscar el usuario por correo
    cursor.execute("SELECT * FROM usuarios WHERE email = %s", (data.email,))
    user = cursor.fetchone()
    
    cursor.close()
    db.close()

    # 3. Validar si el usuario existe
    if not user:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    # 4. Validar la contraseña con bcrypt
    try:
        password_valida = bcrypt.checkpw(
            data.password.encode('utf-8'), 
            user['password'].encode('utf-8')
        )
    except Exception:
        password_valida = False

    if not password_valida:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    # 5. Generar el Token JWT
    token_data = {
        "id": user['id'],
        "email": user['email'],
        "rol": user['rol'],
        "exp": datetime.utcnow() + timedelta(hours=24)
    }
    
    secret_key = os.getenv("SECRET_KEY", "mi_clave_secreta_super_segura")
    token = jwt.encode(token_data, secret_key, algorithm="HS256")

    # 6. Retornar respuesta
    return TokenResponse(
        access_token=token,
        token_type="bearer",
        usuario=UsuarioResponse(
            id=user['id'],
            nombre=user['nombre'],
            email=user['email'],
            rol=user['rol']
        )
    )