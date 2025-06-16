# app/routers/routes_selo.py
from fastapi import APIRouter, Depends, Path, status
from typing import List
from app.controllers import controller_selo as ctrl
from app.models.selo_model import ConcederSeloRequest, SeloConcedido, SolicitarSeloRequest
from app.controllers.token import require_permission, get_current_user, TokenPayLoad

router = APIRouter(
    # O prefixo foi movido para cada rota para maior clareza
    tags=["Selos Concedidos (Instâncias)"],
    responses={404: {"description": "Não encontrado"}},
)

# Rota para um admin conceder um selo a uma empresa

@router.post("/selos/solicitar", status_code=status.HTTP_201_CREATED, summary="Empresa solicita um selo do catálogo", dependencies=[Depends(require_permission("empresa"))])
def solicitar_selo(
    data: SolicitarSeloRequest,
    current_user: TokenPayLoad = Depends(get_current_user)
):
    """
    Cria uma nova solicitação de selo para a empresa associada ao usuário logado.
    A solicitação é criada com o status 'Pendente' e aguarda a aprovação de um administrador.
    """
    return ctrl.solicitar_selo_para_minha_empresa(data, current_user)

@router.post("/empresas/{id_empresa}/selos", status_code=status.HTTP_201_CREATED, summary="Concede um selo a uma empresa", dependencies=[Depends(require_permission("admin", "admin_master"))])
def conceder_selo(id_empresa: int, data: ConcederSeloRequest):
    """
    Associa um tipo de selo do catálogo a uma empresa, criando uma nova instância
    de selo concedido com datas de emissão e expiração.
    """
    return ctrl.conceder_selo_a_empresa(id_empresa, data)

# Rota para listar os selos de uma empresa específica (cliente ou admin)


@router.get("/empresas/{id_empresa}/selos", response_model=List[SeloConcedido], summary="Lista os selos de uma empresa", dependencies=[Depends(require_permission("empresa", "admin", "admin_master"))])
def listar_selos_empresa(id_empresa: int, current_user: TokenPayLoad = Depends(get_current_user)):
    """
    Retorna uma lista de todos os selos (ativos, expirados, etc.) concedidos
    a uma empresa específica. Usuários com perfil 'empresa' só podem ver os seus.
    """
    # A lógica de segurança para impedir que uma empresa veja os selos de outra
    # foi implementada no controller.
    return ctrl.listar_selos_de_empresa(id_empresa, current_user)

# Rota para admin listar solicitações pendentes


@router.get("/selos/solicitacoes", response_model=List[SeloConcedido], summary="Lista todas as solicitações de selo pendentes", dependencies=[Depends(require_permission("admin", "admin_master"))])
def listar_solicitacoes():
    """
    Endpoint para administradores visualizarem todos os selos que estão
    com status 'Pendente' ou 'Em Renovação', aguardando aprovação.
    """
    return ctrl.listar_solicitacoes_pendentes()

# Rota para admin aprovar uma solicitação de selo (pendente ou em renovação)


@router.put("/empresa-selos/{empresa_selo_id}/aprovar", summary="Aprova uma solicitação de selo", dependencies=[Depends(require_permission("admin", "admin_master"))])
def aprovar_selo(empresa_selo_id: int = Path(..., description="O ID da tabela 'empresa_selo'")):
    """
    Muda o status de um selo concedido para 'Ativo' e define suas datas
    de emissão e validade.
    """
    return ctrl.aprovar_selo_concedido(empresa_selo_id)

# Rota para empresa solicitar renovação de um selo


@router.put("/empresa-selos/{empresa_selo_id}/solicitar-renovacao", summary="Solicita a renovação de um selo", dependencies=[Depends(require_permission("empresa"))])
def solicitar_renovacao(
    empresa_selo_id: int = Path(..., description="O ID da tabela 'empresa_selo'"),
    current_user: TokenPayLoad = Depends(get_current_user) # Adicionar esta dependência
):
    """
    Permite que uma empresa solicite a renovação de um selo, mudando seu
    status para 'Em Renovação' para que um administrador possa avaliá-lo.
    """
    return ctrl.solicitar_renovacao_de_selo(empresa_selo_id, current_user)

@router.delete("/empresa-selos/{empresa_selo_id}", status_code=status.HTTP_200_OK, summary="Revoga um selo concedido", dependencies=[Depends(require_permission("admin", "admin_master"))])
def revogar_selo(empresa_selo_id: int = Path(..., description="O ID da instância do selo a ser revogado")):
    """
    Exclui permanentemente a instância de um selo que foi concedido a uma empresa.
    Esta ação é restrita a administradores e não pode ser desfeita.
    """
    return ctrl.revogar_selo_da_empresa(empresa_selo_id)