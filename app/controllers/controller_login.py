from mysql.connector import Error
from datetime import datetime
from typing import Optional
from fastapi import HTTPException
from app.controllers.token import gerar_token
from app.repository.usuario_repository import login_usuario
from app.repository.ibdn_user_repository import repo_get_ibdn_usuario_by_email
from app.repository.ibdn_profiles_repository import repo_get_ibdn_perfil_by_id_with_permissions


from app.security.password import verify_password


def login(email_route: str, senha: str):
    if not email_route or not senha:
        raise HTTPException(
            status_code=400, detail="Email e senha são obrigatórios.")
    """ chamar o bycript """

    print(f"Login attempt for email: {email_route} at {datetime.now()}")

    usuario = repo_get_ibdn_usuario_by_email(
        email_route, include_password_hash=True)

    """ usuario = login_usuario(email_route) """
    if usuario:

        senha_hash = usuario.get("senha_hash")

        if verify_password(senha, senha_hash) is True:

            perfil = usuario.get('perfil_id')
            print(type(perfil))
            
            usuario_id = usuario.get('usuario_id')
            
            permissoes = repo_get_ibdn_perfil_by_id_with_permissions(perfil)
            # O repositório já aninhou o perfil
            if perfil:
                permissoes_do_usuario = [
                    p.get("nome") for p in permissoes.get("permissoes", [])]
            jwt = gerar_token(email_route, permissoes_do_usuario, usuario_id)

            return jwt

        raise HTTPException(status_code=400, detail="Email inválido.")

    if not usuario:
        raise HTTPException(status_code=401, detail="Credenciais inválidas.")
