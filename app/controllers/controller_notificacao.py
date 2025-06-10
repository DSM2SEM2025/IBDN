import mysql.connector
from typing import Optional
from fastapi import HTTPException
from app.database.config import get_db_config
from app.models.notificacao_model import Notificacao, NotificacaoCreate, NotificacaoUpdate
from app.repository.notificacao_repository import (
    get_notificacoes_by_empresa,
    create_notificacao,
    update_notificacao,
    delete_notificacao
)

def get_notificacoes_empresa(empresa_id: int, lida: Optional[bool] = None):
    try:
        notificacoes = get_notificacoes_by_empresa(empresa_id, lida)
        if not notificacoes:
            raise HTTPException(
                status_code=404,
                detail="Nenhuma notificação encontrada para esta empresa"
            )
        return notificacoes
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao buscar notificações: {str(e)}"
        )

def criar_notificacao_empresa(empresa_id: int, notificacao: NotificacaoCreate):
    try:
        notificacao_id = create_notificacao(empresa_id, notificacao.dict())
        return {
            "id": notificacao_id,
            "mensagem": "Notificação criada com sucesso"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao criar notificação: {str(e)}"
        )

def atualizar_notificacao(notificacao_id: int, notificacao: NotificacaoUpdate):
    try:
        updated = update_notificacao(notificacao_id, notificacao.dict(exclude_unset=True))
        if not updated:
            raise HTTPException(
                status_code=404,
                detail="Notificação não encontrada"
            )
        return {"mensagem": "Notificação atualizada com sucesso"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao atualizar notificação: {str(e)}"
        )

def remover_notificacao(notificacao_id: int):
    try:
        deleted = delete_notificacao(notificacao_id)
        if not deleted:
            raise HTTPException(
                status_code=404,
                detail="Notificação não encontrada"
            )
        return {"mensagem": "Notificação removida com sucesso"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao remover notificação: {str(e)}"
        )