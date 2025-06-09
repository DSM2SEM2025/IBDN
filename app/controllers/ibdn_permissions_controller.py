# app/controllers/ibdn_permissions_controller.py
from typing import List, Optional, Dict, Any
from fastapi import HTTPException
from app.repository import ibdn_permissions_repository as repo
from app.models.ibdn_user_model import IbdnPermissaoCreate, IbdnPermissaoUpdate


def create_permissao(permissao_data: IbdnPermissaoCreate) -> Dict[str, Any]:
    return repo.repo_create_ibdn_permissao(permissao_data.model_dump())


def get_permissao(permissao_id: str) -> Optional[Dict[str, Any]]:
    db_permissao = repo.repo_get_ibdn_permissao_by_id(permissao_id)
    if db_permissao is None:
        raise HTTPException(
            status_code=404, detail="Permissão não encontrada.")
    return db_permissao


def get_all_permissoes(skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
    return repo.repo_get_all_ibdn_permissoes(skip=skip, limit=limit)


def update_permissao(permissao_id: str, permissao_data: IbdnPermissaoUpdate) -> Optional[Dict[str, Any]]:
    updated_permissao = repo.repo_update_ibdn_permissao(
        permissao_id, permissao_data.nome)
    if updated_permissao is None:
        raise HTTPException(
            status_code=404, detail="Permissão não encontrada para atualização.")
    return updated_permissao


def delete_permissao(permissao_id: str) -> Dict[str, str]:
    foi_deletado = repo.repo_delete_ibdn_permissao(permissao_id)
    if not foi_deletado:
        raise HTTPException(
            status_code=404, detail="Permissão não encontrada para exclusão.")
    return {"message": "Permissão excluída com sucesso."}
