from fastapi import HTTPException, status
from app.controllers.token import gerar_token
from app.repository.ibdn_user_repository import repo_get_ibdn_usuario_by_email
from app.security.password import verify_password


def login(email_route: str, senha: str):
    """
    Autentica um usuário e retorna um token JWT se as credenciais forem válidas.
    """
    if not email_route or not senha:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email e senha são obrigatórios."
        )

    # Busca o usuário pelo e-mail, incluindo o hash da senha para verificação
    usuario = repo_get_ibdn_usuario_by_email(
        email_route, include_password_hash=True)

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas."
        )

    senha_hash = usuario.get("senha_hash")
    if not senha_hash or not verify_password(senha, senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas."
        )

    # Extrai as informações necessárias para o token
    usuario_id = usuario.get('id')
    # Adicionado na query do repositório
    empresa_id = usuario.get('empresa_id')
    permissoes_do_usuario = []

    # O perfil e as permissões já vêm aninhados do repositório
    perfil_do_usuario = usuario.get("perfil")
    if perfil_do_usuario and perfil_do_usuario.get("permissoes"):
        permissoes_do_usuario = [
            p.get("nome") for p in perfil_do_usuario["permissoes"] if p.get("nome")
        ]

    # Gera o token com todos os dados necessários
    jwt = gerar_token(
        email=email_route,
        usuario_id=usuario_id,
        permissoes=permissoes_do_usuario,
        empresa_id=empresa_id
    )

    return jwt
