# app/controllers/ibdn_users_controller.py
from typing import List, Optional, Dict, Any
from fastapi import HTTPException
from app.repository import ibdn_user_repository as repo_users
# Para validar perfil_id
from app.repository import ibdn_profiles_repository as repo_profiles
from app.models.ibdn_user_model import IbdnUsuarioCreate, IbdnUsuarioUpdate


def create_usuario(usuario_data: IbdnUsuarioCreate) -> Optional[Dict[str, Any]]:
    # Verificar se o email já existe (o repositório também verifica, mas pode ser feito aqui)
    existing_user_by_email = repo_users.repo_get_ibdn_usuario_by_email(
        usuario_data.email)
    if existing_user_by_email:
        raise HTTPException(
            status_code=409, detail=f"Usuário com email '{usuario_data.email}' já existe.")

    # Verificar se o perfil_id existe, se fornecido
    if usuario_data.perfil_id:
        if not repo_profiles.repo_get_ibdn_perfil_by_id_with_permissions(usuario_data.perfil_id):
            raise HTTPException(
                status_code=404, detail=f"Perfil com ID '{usuario_data.perfil_id}' não encontrado.")

    return repo_users.repo_create_ibdn_usuario(usuario_data)


def get_usuario(usuario_id: str) -> Optional[Dict[str, Any]]:
    db_usuario = repo_users.repo_get_ibdn_usuario_by_id(usuario_id)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    return db_usuario


def get_all_usuarios(skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
    return repo_users.repo_get_all_ibdn_usuarios(skip=skip, limit=limit)


def update_usuario(usuario_id: str, usuario_data: IbdnUsuarioUpdate) -> Optional[Dict[str, Any]]:
    # Verificar se o usuário a ser atualizado existe
    if not repo_users.repo_get_ibdn_usuario_by_id(usuario_id):
        raise HTTPException(
            status_code=404, detail="Usuário não encontrado para atualização.")

    # Se o email estiver sendo alterado, verificar se o novo email já está em uso por OUTRO usuário
    if usuario_data.email:
        user_with_new_email = repo_users.repo_get_ibdn_usuario_by_email(
            usuario_data.email)
        if user_with_new_email and user_with_new_email.get("id") != usuario_id:
            raise HTTPException(
                status_code=409, detail=f"O email '{usuario_data.email}' já está em uso por outro usuário.")

    # Verificar se o perfil_id existe, se fornecido e diferente de None
    # Se for None, significa desvincular (válido)
    if usuario_data.perfil_id is not None:
        if not repo_profiles.repo_get_ibdn_perfil_by_id_with_permissions(usuario_data.perfil_id):
            raise HTTPException(
                status_code=404, detail=f"Perfil com ID '{usuario_data.perfil_id}' não encontrado.")

    updated_usuario = repo_users.repo_update_ibdn_usuario(
        usuario_id, usuario_data)
    if updated_usuario is None:  # Segurança extra, já que a primeira verificação deveria pegar
        raise HTTPException(
            status_code=404, detail="Usuário não encontrado após tentativa de atualização.")
    return updated_usuario


def delete_usuario(usuario_id: str) -> Dict[str, str]:
    # Verifica se existe antes
    if not repo_users.repo_get_ibdn_usuario_by_id(usuario_id):
        raise HTTPException(
            status_code=404, detail="Usuário não encontrado para exclusão.")

    if not repo_users.repo_delete_ibdn_usuario(usuario_id):
        # Esta condição pode não ser alcançada se o repo_delete_ibdn_usuario levantar exceção
        raise HTTPException(
            status_code=500, detail="Falha ao excluir o usuário.")
    return {"message": "Usuário excluído com sucesso."}
