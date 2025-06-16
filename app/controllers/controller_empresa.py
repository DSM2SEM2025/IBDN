# app/controllers/controller_empresa.py
from fastapi import HTTPException, status
from typing import List, Dict, Any
from app.models.empresas_model import (
    Empresa, EmpresaCreate, EmpresaUpdate
)
from app.controllers.token import TokenPayLoad
from app.repository import empresa_repository as repo_empresa
from app.repository import ibdn_user_repository


def get_empresas() -> List[Empresa]:
    """
    Controller para buscar todas as empresas ativas.
    A permissão de acesso é validada diretamente na rota.
    """
    try:
        empresas_db = repo_empresa.repo_get_all_empresas()
        return [Empresa(**empresa) for empresa in empresas_db]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar empresas: {e}"
        )


def get_empresa_por_id(empresa_id: int, current_user: TokenPayLoad) -> Empresa:
    """
    Controller para buscar uma empresa específica pelo ID, aplicando regras de permissão.
    - Admins ('admin', 'admin_master') podem ver qualquer empresa.
    - Usuários com perfil 'empresa' podem ver apenas a sua própria empresa.
    """
    try:
        # Primeiro, sempre buscamos a empresa no banco de dados.

        permissoes_usuario = set(current_user.permissoes)
        is_admin = bool(permissoes_usuario.intersection(
            {"admin", "admin_master"}))

        empresa_db = repo_empresa.repo_get_empresa_by_id(empresa_id)
        if not empresa_db and is_admin:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Empresa não encontrada"
            )
        if not empresa_db:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Você não tem permissão para acessar os dados desta empresa."
            )

        # CORREÇÃO DA LÓGICA DE SEGURANÇA:
        # Validamos a titularidade usando o 'usuario_id' do banco de dados.
        # Se o usuário não for admin E o 'usuario_id' da empresa no banco for diferente
        # do 'usuario_id' do usuário logado (no token), o acesso é negado.
        if not is_admin and empresa_db['usuario_id'] != current_user.usuario_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Você não tem permissão para acessar os dados desta empresa."
            )

        # Se passou na verificação, retorna os dados da empresa.
        return Empresa(**empresa_db)

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar empresa: {e}"
        )


def criar_empresa(empresa_data: EmpresaCreate, current_user: TokenPayLoad) -> Dict[str, Any]:
    """
    Controller para criar uma nova empresa com base nas permissões do usuário.
    """
    permissoes_usuario = set(current_user.permissoes)
    is_admin = bool(permissoes_usuario.intersection({"admin", "admin_master"}))
    usuario_id_associado = None

    if is_admin:
        # Se for admin e um usuario_id foi fornecido, usa-o.
        if empresa_data.usuario_id:
            usuario_alvo = ibdn_user_repository.repo_get_ibdn_usuario_by_id(
                empresa_data.usuario_id)
            if not usuario_alvo:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail=f"Usuário com ID {empresa_data.usuario_id} não encontrado.")
            usuario_id_associado = empresa_data.usuario_id
        else:
            # Se for admin mas não forneceu um ID, associa a ele mesmo.
            usuario_id_associado = current_user.usuario_id
    else:
        # Se não for admin, verifica se já tem uma empresa. Se tiver, não pode criar outra.
        if current_user.empresa_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Você já está associado a uma empresa.")
        # Se não tiver, a nova empresa será associada ao seu próprio ID.
        usuario_id_associado = current_user.usuario_id

    try:
        nova_empresa_id = repo_empresa.repo_criar_nova_empresa(
            empresa_data, usuario_id_associado)
        return {"id": nova_empresa_id, "mensagem": "Empresa criada com sucesso"}

    except Exception as e:
        # Conflito, como CNPJ duplicado.
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

    # Apenas admins podem ativar/inativar uma empresa.
    if empresa_data.ativo is not None and not is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Apenas administradores podem alterar o status da empresa.")

    # Usuários 'empresa' só podem atualizar os dados da sua própria empresa.
    if not is_admin and empresa_existente['usuario_id'] != current_user.usuario_id:
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
    """
    Aplica permissões e realiza a exclusão lógica (inativação) da empresa.
    A permissão de acesso é validada diretamente na rota (apenas admins).
    """
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
