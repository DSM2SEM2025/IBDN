# app/controllers/ibdn_profiles_controller.py
from typing import List, Optional, Dict, Any
from fastapi import HTTPException
from app.repository import ibdn_profiles_repository as repo_profiles
# Para validar IDs de permissão
from app.repository import ibdn_permissions_repository as repo_perms
from app.models.ibdn_user_model import IbdnPerfilCreate, IbdnPerfilUpdate, PerfilPermissaoLink


def create_perfil(perfil_data: IbdnPerfilCreate) -> Optional[Dict[str, Any]]:
    if perfil_data.permissoes_ids:
        for p_id in perfil_data.permissoes_ids:
            if not repo_perms.repo_get_ibdn_permissao_by_id(p_id):
                raise HTTPException(
                    status_code=404, detail=f"Permissão com ID '{p_id}' não encontrada.")

    created_data = repo_profiles.repo_create_ibdn_perfil(
        perfil_data.model_dump(exclude={'permissoes_ids'}),
        perfil_data.permissoes_ids
    )
    return repo_profiles.repo_get_ibdn_perfil_by_id_with_permissions(created_data['id'])


def get_perfil(perfil_id: str) -> Optional[Dict[str, Any]]:
    db_perfil = repo_profiles.repo_get_ibdn_perfil_by_id_with_permissions(
        perfil_id)
    if db_perfil is None:
        raise HTTPException(status_code=404, detail="Perfil não encontrado.")
    return db_perfil


def get_all_perfis(skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
    return repo_profiles.repo_get_all_ibdn_perfis_with_permissions(skip=skip, limit=limit)


def update_perfil(perfil_id: str, perfil_update_data: IbdnPerfilUpdate) -> Optional[Dict[str, Any]]:
    # Verifica se o perfil existe antes de tentar qualquer coisa
    if not repo_profiles.repo_get_ibdn_perfil_by_id_with_permissions(perfil_id):
        raise HTTPException(
            status_code=404, detail="Perfil não encontrado para atualização.")

    if perfil_update_data.permissoes_ids is not None:
        for p_id in perfil_update_data.permissoes_ids:
            if not repo_perms.repo_get_ibdn_permissao_by_id(p_id):
                raise HTTPException(
                    status_code=404, detail=f"Permissão com ID '{p_id}' não encontrada para associação.")

    updated_perfil = repo_profiles.repo_update_ibdn_perfil(
        perfil_id,
        perfil_update_data.nome,
        perfil_update_data.permissoes_ids
    )
    if updated_perfil is None:  # Deveria ser pego pela verificação inicial, mas é uma segurança
        raise HTTPException(
            status_code=404, detail="Perfil não encontrado após tentativa de atualização.")
    return updated_perfil


def delete_perfil(perfil_id: str) -> Dict[str, str]:
    if not repo_profiles.repo_get_ibdn_perfil_by_id_with_permissions(perfil_id):
        raise HTTPException(
            status_code=404, detail="Perfil não encontrado para exclusão.")

    if not repo_profiles.repo_delete_ibdn_perfil(perfil_id):
        raise HTTPException(
            status_code=500, detail="Falha ao excluir o perfil.")
    return {"message": "Perfil excluído com sucesso."}


def add_permissao_to_perfil_ctrl(perfil_id: str, link_data: PerfilPermissaoLink) -> Optional[Dict[str, Any]]:
    if not repo_profiles.repo_get_ibdn_perfil_by_id_with_permissions(perfil_id):
        raise HTTPException(status_code=404, detail="Perfil não encontrado.")
    if not repo_perms.repo_get_ibdn_permissao_by_id(link_data.permissao_id):
        raise HTTPException(
            status_code=404, detail="Permissão não encontrada.")

    repo_profiles.repo_add_permissao_to_perfil(
        perfil_id, link_data.permissao_id)
    return repo_profiles.repo_get_ibdn_perfil_by_id_with_permissions(perfil_id)


def remove_permissao_from_perfil_ctrl(perfil_id: str, permissao_id: str) -> Optional[Dict[str, Any]]:
    if not repo_profiles.repo_get_ibdn_perfil_by_id_with_permissions(perfil_id):
        raise HTTPException(status_code=404, detail="Perfil não encontrado.")
    # Opcional: verificar se a permissão existe, embora o DELETE não falhe se não existir a permissão em si
    # if not repo_perms.repo_get_ibdn_permissao_by_id(permissao_id):
    #     raise HTTPException(status_code=404, detail="Permissão não encontrada para desvincular.")

    repo_profiles.repo_remove_permissao_from_perfil(perfil_id, permissao_id)
    # Mesmo que a permissão não estivesse associada, retornamos o estado atual do perfil
    return repo_profiles.repo_get_ibdn_perfil_by_id_with_permissions(perfil_id)
