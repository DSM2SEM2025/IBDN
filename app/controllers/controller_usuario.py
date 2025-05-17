from mysql.connector import Error
from datetime import datetime
from typing import Optional
from fastapi import HTTPException
from app.repository.usuario_repository import login_usuario
import bcrypt

from app.security.password import verificar_senha


async def login(email: str, senha: str):
    if not email or not senha:
        raise HTTPException(
            status_code=400, detail="Email e senha são obrigatórios.")
    """ chamar o bycript """

    usuario = login_usuario(email, senha)

    autentificado = verificar_senha(senha, usuario['senha_hash'])
    print(f"aqui : {autentificado}")
    return "oi"
