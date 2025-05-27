from mysql.connector import Error
from datetime import datetime
from typing import Optional
from fastapi import HTTPException
from app.controllers.token import gerar_token
from app.repository.usuario_repository import login_usuario
import bcrypt

from app.security.password import verificar_senha


def login(email_route: str, senha: str):
    if not email_route or not senha:
        raise HTTPException(
            status_code=400, detail="Email e senha são obrigatórios.")
    """ chamar o bycript """

    usuario = login_usuario(email_route)
    if usuario:
        senha_hash = usuario.get("senha_hash")

        if verificar_senha(senha, senha_hash) is True:
            perfil = usuario.get('perfil')

            jwt = gerar_token(email_route, perfil)

            return jwt

        raise HTTPException(status_code=400, detail="Email inválido.")

    if not usuario:
        raise HTTPException(status_code=401, detail="Credenciais inválidas.")
