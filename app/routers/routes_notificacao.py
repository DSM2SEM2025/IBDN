from fastapi import APIRouter, Path, Query, Depends, status
from typing import List, Optional
from app.controllers.controller_notificacao import (
    get_notificacoes_empresa,
    criar_notificacao_empresa,
    atualizar_notificacao as atualizar_notificacao_controller,
    remover_notificacao
)
from app.models.notificacao_model import Notificacao, NotificacaoCreate, NotificacaoUpdate
from app.controllers.token import require_permission, get_current_user, TokenPayLoad

router = APIRouter(
    tags=["Notificações"],
    responses={404: {"description": "Não encontrado"}},
)

@router.get("/empresas/{empresa_id}/notificacoes", response_model=List[Notificacao], summary="Lista as notificações de uma empresa", dependencies=[Depends(require_permission("empresa", "admin", "admin_master"))])
def listar_notificacoes_empresa(
    empresa_id: int = Path(..., gt=0),
    lida: Optional[bool] = Query(None, description="Filtre as notificações por status de leitura (true para lidas, false para não lidas)."),
    current_user: TokenPayLoad = Depends(get_current_user)
):
    return get_notificacoes_empresa(empresa_id, current_user, lida)

@router.post("/empresas/{empresa_id}/notificacoes", response_model=dict, status_code=status.HTTP_201_CREATED, summary="Admin cria uma notificação para uma empresa", dependencies=[Depends(require_permission("admin", "admin_master"))])
def criar_notificacao(
    notificacao: NotificacaoCreate,
    empresa_id: int = Path(..., gt=0)
):
    return criar_notificacao_empresa(empresa_id, notificacao)

@router.put("/notificacoes/{notificacao_id}", response_model=dict, summary="Atualiza uma notificação (marcar como lida)", dependencies=[Depends(require_permission("empresa", "admin", "admin_master"))])
def atualizar_notificacao(
    notificacao: NotificacaoUpdate,
    notificacao_id: int = Path(..., gt=0),
    current_user: TokenPayLoad = Depends(get_current_user)
):
    return atualizar_notificacao_controller(notificacao_id, notificacao, current_user)

@router.delete("/notificacoes/{notificacao_id}", response_model=dict, summary="Admin remove uma notificação", dependencies=[Depends(require_permission("admin", "admin_master"))])
def deletar_notificacao(
    notificacao_id: int = Path(..., gt=0)
):
    return remover_notificacao(notificacao_id)
