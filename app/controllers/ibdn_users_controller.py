from typing import List, Optional, Dict, Any
from fastapi import HTTPException, status
from app.repository import ibdn_user_repository as repo_users
from app.repository import ibdn_profiles_repository as repo_profiles
from app.models.ibdn_user_model import IbdnUsuarioCreate, IbdnUsuarioUpdate, UsuarioRegister, IbdnUsuario
from app.controllers.token import TokenPayLoad


def register_new_user(usuario_data: UsuarioRegister) -> IbdnUsuario:
    existing_user = repo_users.repo_get_ibdn_usuario_by_email(usuario_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="O e-mail fornecido já está cadastrado no sistema."
        )

    user_to_create = IbdnUsuarioCreate(
        nome=usuario_data.nome,
        email=usuario_data.email,
        senha=usuario_data.senha
    )
    
    created_user_data = repo_users.repo_create_ibdn_usuario(user_to_create)
    if not created_user_data:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocorreu um erro ao criar o usuário. Tente novamente."
        )

    return IbdnUsuario(**created_user_data)

def create_usuario(usuario_data: IbdnUsuarioCreate) -> Optional[Dict[str, Any]]:
    existing_user_by_email = repo_users.repo_get_ibdn_usuario_by_email(
        usuario_data.email)
    if existing_user_by_email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=f"Usuário com email '{usuario_data.email}' já existe.")

    if usuario_data.perfil_id:
        if not repo_profiles.repo_get_ibdn_perfil_by_id_with_permissions(usuario_data.perfil_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Perfil com ID '{usuario_data.perfil_id}' não encontrado.")

    return repo_users.repo_create_ibdn_usuario(usuario_data)


def get_usuario(usuario_id: str, current_user: TokenPayLoad) -> Optional[Dict[str, Any]]:
    permissoes_usuario = set(current_user.permissoes)
    is_admin = bool(permissoes_usuario.intersection({"admin", "admin_master"}))

    if not is_admin and current_user.usuario_id != usuario_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para visualizar este usuário."
        )

    db_usuario = repo_users.repo_get_ibdn_usuario_by_id(usuario_id)
    if db_usuario is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Usuário não encontrado.")
    return db_usuario


def get_all_usuarios(skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
    return repo_users.repo_get_all_ibdn_usuarios(skip=skip, limit=limit)


def update_usuario(usuario_id: str, usuario_data: IbdnUsuarioUpdate, current_user: TokenPayLoad) -> Optional[Dict[str, Any]]:
    permissoes_usuario = set(current_user.permissoes)
    is_admin = bool(permissoes_usuario.intersection({"admin", "admin_master"}))

    if not is_admin and current_user.usuario_id != usuario_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para atualizar este usuário."
        )

    if not repo_users.repo_get_ibdn_usuario_by_id(usuario_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado para atualização.")

    if usuario_data.email:
        user_with_new_email = repo_users.repo_get_ibdn_usuario_by_email(
            usuario_data.email)
        if user_with_new_email and user_with_new_email.get("id") != usuario_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail=f"O email '{usuario_data.email}' já está em uso por outro usuário.")

    if usuario_data.perfil_id is not None:
        if not repo_profiles.repo_get_ibdn_perfil_by_id_with_permissions(usuario_data.perfil_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Perfil com ID '{usuario_data.perfil_id}' não encontrado.")

    updated_usuario = repo_users.repo_update_ibdn_usuario(
        usuario_id, usuario_data)
    if updated_usuario is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado após tentativa de atualização.")
    return updated_usuario


def delete_usuario(usuario_id: str) -> Dict[str, str]:
    if not repo_users.repo_get_ibdn_usuario_by_id(usuario_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado para exclusão.")

    if not repo_users.repo_delete_ibdn_usuario(usuario_id):
        raise HTTPException(
            status_code=status.HTTP_500, detail="Falha ao excluir o usuário.")
    return {"message": "Usuário excluído com sucesso."}