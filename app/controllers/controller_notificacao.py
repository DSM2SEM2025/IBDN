from fastapi import HTTPException, status
from typing import Optional, List
from app.models.notificacao_model import Notificacao, NotificacaoCreate, NotificacaoUpdate
from app.repository import notificacao_repository as repo
from app.controllers.token import TokenPayLoad

def get_notificacoes_empresa(empresa_id: int, current_user: TokenPayLoad, lida: Optional[bool] = None) -> List[Notificacao]:
    is_admin = "admin" in current_user.permissoes or "admin_master" in current_user.permissoes
    if not is_admin and current_user.empresa_id != empresa_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para visualizar as notificações desta empresa."
        )
    notificacoes_db = repo.get_notificacoes_by_empresa(empresa_id, lida)
    return [Notificacao(**notificacao) for notificacao in notificacoes_db]

def criar_notificacao_empresa(empresa_id: int, notificacao: NotificacaoCreate) -> dict:
    notificacao_id = repo.create_notificacao(empresa_id, notificacao.model_dump())
    return {"id": notificacao_id, "mensagem": "Notificação criada com sucesso"}

def atualizar_notificacao(notificacao_id: int, notificacao: NotificacaoUpdate, current_user: TokenPayLoad) -> dict:
    notificacao_existente = repo.get_notificacao_by_id(notificacao_id)
    if not notificacao_existente:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notificação não encontrada")

    is_admin = "admin" in current_user.permissoes or "admin_master" in current_user.permissoes

    if not is_admin:
        if notificacao_existente['id_empresa'] != current_user.empresa_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permissão negada para alterar esta notificação.")
        
        update_data = notificacao.model_dump(exclude_unset=True)
        if list(update_data.keys()) != ['lida']:
             raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Você só tem permissão para marcar a notificação como lida.")

    repo.update_notificacao(notificacao_id, notificacao.model_dump(exclude_unset=True))
    return {"mensagem": "Notificação atualizada com sucesso"}

def remover_notificacao(notificacao_id: int) -> dict:
    deleted = repo.delete_notificacao(notificacao_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notificação não encontrada")
    return {"mensagem": "Notificação removida com sucesso"}