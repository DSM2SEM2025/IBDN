# app/controllers/tipo_selo_controller.py
from fastapi import HTTPException, status
from typing import List
from app.models.tipo_selo_model import TipoSeloCreate, TipoSeloUpdate, TipoSeloInDB
from app.repository import tipo_selo_repository as repo


def create_tipo_selo(data: TipoSeloCreate) -> TipoSeloInDB:
    try:
        new_id = repo.repo_create_tipo_selo(data)
        # Retorna o objeto completo, incluindo o ID gerado e os dados enviados
        return TipoSeloInDB(id=new_id, **data.model_dump())
    except Exception as e:
        # Trata erros específicos que podem vir do banco, como sigla duplicada
        if "UNIQUE constraint" in str(e) or "Duplicate entry" in str(e):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"Já existe um tipo de selo com a mesma sigla ou nome.")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


def get_all_tipos_selo() -> List[TipoSeloInDB]:
    tipos_selo_db = repo.repo_get_all_tipos_selo()
    return [TipoSeloInDB(**selo) for selo in tipos_selo_db]


def get_tipo_selo_by_id(id: int) -> TipoSeloInDB:
    selo = repo.repo_get_tipo_selo_by_id(id)
    if not selo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Tipo de Selo não encontrado")
    return selo


def update_tipo_selo(id: int, data: TipoSeloUpdate) -> TipoSeloInDB:
    # Primeiro, verifica se o tipo de selo existe
    existing_selo = repo.repo_get_tipo_selo_by_id(id)
    if not existing_selo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Tipo de Selo não encontrado para atualização")

    # Realiza a atualização
    repo.repo_update_tipo_selo(id, data)

    # Retorna os dados atualizados
    return get_tipo_selo_by_id(id)


def delete_tipo_selo(id: int):
    """
    Controller para inativar (soft delete) um tipo de selo.
    """
    # A função do repositório agora retorna False se o selo não foi encontrado ou já estava inativo.
    if not repo.repo_delete_tipo_selo(id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Tipo de Selo não encontrado ou já está inativo.")

    # CORREÇÃO: Mensagem de sucesso reflete a ação de inativar.
    return {"message": "Tipo de Selo inativado com sucesso."}
