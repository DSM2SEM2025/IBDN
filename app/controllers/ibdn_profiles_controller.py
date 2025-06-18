from typing import List, Optional, Dict, Any
from fastapi import HTTPException
from app.repository import ibdn_profiles_repository as repo_profiles
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
    return updated_perfil


def delete_perfil(perfil_id: str) -> Dict[str, str]:
    foi_deletado = repo_profiles.repo_delete_ibdn_perfil(perfil_id)
    if not foi_deletado:
        raise HTTPException(
            status_code=404, detail="Perfil não encontrado para exclusão.")
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

    repo_profiles.repo_remove_permissao_from_perfil(perfil_id, permissao_id)
    return repo_profiles.repo_get_ibdn_perfil_by_id_with_permissions(perfil_id)