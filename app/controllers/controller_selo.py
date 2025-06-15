# app/controllers/controller_selo.py
from fastapi import HTTPException, status
from typing import List
from app.models.selo_model import SeloCreate, SeloUpdate, SeloInDB, ConcederSeloRequest, SeloConcedido
# CORREÇÃO: O nome do arquivo importado agora está no plural para corresponder ao nome do arquivo real.
from app.repository import selos_repository as repo

# --- Controller para o Catálogo de Selos ---


def criar_tipo_selo(data: SeloCreate) -> SeloInDB:
    """Cria um novo tipo de selo no catálogo (gerenciado por admins)."""
    try:
        new_id = repo.repo_criar_selo(data.model_dump())
        return SeloInDB(id=new_id, **data.model_dump())
    except HTTPException as e:
        raise e


def listar_tipos_selo() -> List[SeloInDB]:
    """Lista todos os tipos de selo disponíveis no catálogo."""
    selos_db = repo.repo_listar_selos()
    return [SeloInDB(**selo) for selo in selos_db]

# --- Controller para Instâncias de Selos Concedidos ---


def conceder_selo_a_empresa(id_empresa: int, data: ConcederSeloRequest) -> dict:
    """Concede um selo de um tipo existente a uma empresa específica."""
    try:
        return repo.repo_conceder_selo_empresa(id_empresa, data.id_selo, data.dias_validade)
    except HTTPException as e:
        raise e


def listar_selos_de_empresa(id_empresa: int) -> List[SeloConcedido]:
    """Lista todas as instâncias de selos que uma empresa possui."""
    selos_db = repo.repo_listar_selos_da_empresa(id_empresa)
    return [SeloConcedido(**selo) for selo in selos_db]


def listar_solicitacoes_pendentes() -> List[SeloConcedido]:
    """Retorna uma lista de todos os selos que estão aguardando aprovação."""
    solicitacoes_db = repo.repo_listar_solicitacoes_pendentes()
    return [SeloConcedido(**solicitacao) for solicitacao in solicitacoes_db]


def aprovar_selo_concedido(empresa_selo_id: int) -> dict:
    """Aprova uma solicitação de selo, mudando seu status para 'Ativo' e atualizando as datas."""
    sucesso = repo.repo_atualizar_status_selo(empresa_selo_id, 'Ativo')
    if not sucesso:
        raise HTTPException(
            status_code=404, detail="Selo concedido não encontrado ou já está ativo.")
    return {"message": "Selo aprovado e ativado com sucesso."}


def solicitar_renovacao_de_selo(empresa_selo_id: int) -> dict:
    """Muda o status de um selo para 'Em Renovação' para que um admin possa reavaliá-lo."""
    # A lógica aqui poderia verificar se o selo está 'Expirado' antes de permitir a renovação
    sucesso = repo.repo_atualizar_status_selo(empresa_selo_id, 'Em Renovação')
    if not sucesso:
        raise HTTPException(
            status_code=404, detail="Selo concedido não encontrado.")
    return {"message": "Solicitação de renovação enviada com sucesso."}
