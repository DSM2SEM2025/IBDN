from fastapi import APIRouter, Path, Query
from typing import List, Optional
from app.controllers.controller_notificacao import (
    get_notificacoes_empresa,
    criar_notificacao_empresa,
    atualizar_notificacao,
    remover_notificacao
)
from app.models.notificacao_model import (
    Notificacao,
    NotificacaoCreate,
    NotificacaoUpdate
)

router = APIRouter(
    prefix="",
    tags=["Notificacoes"],
    responses={404: {"description": "Não encontrado"}},
)

@router.get("/empresas/{empresa_id}/notificacoes", response_model=List[Notificacao])
def listar_notificacoes_empresa(
    empresa_id: int = Path(..., gt=0),
    lida: Optional[bool] = Query(None)
):
    return get_notificacoes_empresa(empresa_id, lida)

@router.post("/empresas/{empresa_id}/notificacoes", response_model=dict)
def criar_notificacao(
    notificacao: NotificacaoCreate,
    empresa_id: int = Path(..., gt=0)
    
):
    return criar_notificacao_empresa(empresa_id, notificacao)

@router.put("/notificacoes/{notificacao_id}", response_model=dict)
def atualizar_notificacao(
    notificacao: NotificacaoUpdate,
    notificacao_id: int = Path(..., gt=0)
    
):
    return atualizar_notificacao(notificacao_id, notificacao)

@router.delete("/notificacoes/{notificacao_id}", response_model=dict)
def deletar_notificacao(
    notificacao_id: int = Path(..., gt=0)
):
    return remover_notificacao(notificacao_id)