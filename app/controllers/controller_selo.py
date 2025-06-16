# app/controllers/controller_selo.py
from fastapi import HTTPException, status
from typing import List
from app.models.selo_model import SeloCreate, SeloUpdate, SeloInDB, ConcederSeloRequest, SeloConcedido, SolicitarSeloRequest

# CORREÇÃO: O nome do arquivo importado agora está no plural para corresponder ao nome do arquivo real.
from app.repository import selos_repository as repo
from app.controllers.token import TokenPayLoad


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


def listar_selos_de_empresa(id_empresa: int, current_user: TokenPayLoad) -> List[SeloConcedido]:
    """Lista todas as instâncias de selos que uma empresa possui, com verificação de permissão."""
    
    # --- BLOCO DE SEGURANÇA ---
    # Verifica se o usuário é admin. Se não for, ele só pode ver os dados da sua própria empresa.
    is_admin = "admin" in current_user.permissoes or "admin_master" in current_user.permissoes
    if not is_admin and current_user.empresa_id != id_empresa:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para visualizar os selos desta empresa."
        )
    # --- FIM DO BLOCO DE SEGURANÇA ---

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


def solicitar_renovacao_de_selo(empresa_selo_id: int, current_user: TokenPayLoad) -> dict:
    """Muda o status de um selo para 'Em Renovação' para que um admin possa reavaliá-lo."""
    
    # --- BLOCO DE SEGURANÇA ---
    # 1. Busca os dados da instância do selo
    selo_concedido = repo.repo_get_empresa_selo_por_id(empresa_selo_id)
    if not selo_concedido:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Selo concedido não encontrado.")

    # 2. Verifica se a empresa do selo é a mesma do usuário logado
    if selo_concedido['id_empresa'] != current_user.empresa_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para solicitar a renovação deste selo."
        )
    # --- FIM DO BLOCO DE SEGURANÇA ---

    # A lógica original pode prosseguir, pois a titularidade foi verificada
    sucesso = repo.repo_atualizar_status_selo(empresa_selo_id, 'Em Renovação')
    if not sucesso:
        raise HTTPException(
            status_code=404, detail="Não foi possível solicitar a renovação. Selo não encontrado ou status inválido.")
            
    return {"message": "Solicitação de renovação enviada com sucesso."}

def revogar_selo_da_empresa(empresa_selo_id: int) -> dict:
    """
    Revoga (exclui) um selo que foi concedido a uma empresa.
    Apenas administradores podem realizar esta ação.
    """
    # Verifica se a instância do selo existe antes de tentar deletar
    selo_existente = repo.repo_get_empresa_selo_por_id(empresa_selo_id)
    if not selo_existente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Selo concedido não encontrado para revogação."
        )

    # Se existir, prossegue com a exclusão
    sucesso = repo.repo_revogar_selo_empresa(empresa_selo_id)
    if not sucesso:
        # Medida de segurança caso a exclusão falhe por um motivo inesperado
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocorreu um erro ao tentar revogar o selo."
        )

    return {"message": "Selo revogado com sucesso."}

def solicitar_selo_para_minha_empresa(data: SolicitarSeloRequest, current_user: TokenPayLoad) -> dict:
    """
    Permite que um usuário logado (perfil empresa) solicite um selo para sua própria empresa.
    """
    # Adiciona uma verificação explícita para garantir que o usuário tem a permissão 'empresa'.
    if "empresa" not in current_user.permissoes:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Esta ação é permitida apenas para usuários do tipo empresa."
        )

    id_empresa = current_user.empresa_id
    if not id_empresa:
        # Esta verificação agora serve como uma segurança secundária.
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuário do tipo empresa não está associado a nenhuma empresa."
        )
    return repo.repo_solicitar_selo_empresa(id_empresa, data.id_selo)
