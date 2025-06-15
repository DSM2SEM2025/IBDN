from fastapi import HTTPException, status
from typing import List, Dict, Any
from app.models.empresas_model import (
    Empresa, EmpresaCreate, EmpresaUpdate
)
from app.controllers.token import TokenPayLoad
from app.repository import empresa_repository as repo_empresa
from app.repository import ibdn_user_repository


def get_empresas() -> List[Empresa]:
    """Busca todas as empresas ativas através do repositório."""
    try:
        empresas_db = repo_empresa.repo_get_all_empresas()
        return [Empresa(**empresa) for empresa in empresas_db]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar empresas: {e}"
        )


def get_empresa_por_id(empresa_id: int) -> Empresa:
    """Busca uma empresa específica pelo ID."""
    try:
        empresa_db = repo_empresa.repo_get_empresa_by_id(empresa_id)
        if not empresa_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Empresa não encontrada"
            )
        return Empresa(**empresa_db)
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar empresa: {e}"
        )


# Removido o 'async'
def criar_empresa(empresa_data: EmpresaCreate, current_user: TokenPayLoad) -> Dict[str, Any]:
    """
    Controller para criar uma nova empresa com base nas permissões do usuário.
    """
    permissoes_usuario = set(current_user.permissoes)
    usuario_id_associado = None

    if "admin" in permissoes_usuario or "admin_master" in permissoes_usuario:
        if empresa_data.usuario_id:
            usuario_alvo = ibdn_user_repository.repo_get_ibdn_usuario_by_id(
                empresa_data.usuario_id)
            if not usuario_alvo:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail=f"Usuário com ID {empresa_data.usuario_id} não encontrado.")
            usuario_id_associado = empresa_data.usuario_id
        else:
            usuario_id_associado = current_user.usuario_id
    else:
        if current_user.empresa_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Você já está associado a uma empresa.")
        usuario_id_associado = current_user.usuario_id

    try:
        # A chamada aqui agora é síncrona
        nova_empresa_id = repo_empresa.repo_criar_nova_empresa(
            empresa_data, usuario_id_associado)
        return {"id": nova_empresa_id, "mensagem": "Empresa criada com sucesso"}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=str(e))


def update_empresa(id_empresa: int, empresa_data: EmpresaUpdate, current_user: TokenPayLoad) -> Empresa:
    """Aplica permissões e atualiza a empresa."""
    empresa_existente = repo_empresa.repo_get_empresa_by_id(id_empresa)
    if not empresa_existente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Empresa com ID {id_empresa} não encontrada."
        )

    permissoes_usuario = set(current_user.permissoes)
    is_admin = bool(permissoes_usuario.intersection({"admin", "admin_master"}))

    if empresa_data.ativo is not None and not is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Apenas administradores podem alterar o status da empresa.")

    if not is_admin and current_user.empresa_id != id_empresa:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Permissão negada: você só pode atualizar dados da sua própria empresa.")

    try:
        repo_empresa.repo_update_empresa(id_empresa, empresa_data)
        empresa_atualizada = repo_empresa.repo_get_empresa_by_id(id_empresa)
        return Empresa(**empresa_atualizada)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


def delete_empresa(empresa_id: int, current_user: TokenPayLoad) -> dict:
    """Aplica permissões e realiza a exclusão lógica da empresa."""
    empresa_existente = repo_empresa.repo_get_empresa_by_id(empresa_id)
    if not empresa_existente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Empresa com ID {empresa_id} não encontrada."
        )

    if not empresa_existente['ativo']:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Empresa com ID {empresa_id} já se encontra inativa."
        )

    try:
        sucesso = repo_empresa.repo_delete_empresa(empresa_id)
        if not sucesso:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Falha ao inativar empresa. Talvez já estivesse inativa.")

        return {"mensagem": "Empresa inativada com sucesso."}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
