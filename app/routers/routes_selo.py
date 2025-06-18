from fastapi import APIRouter, Depends, Path, status
from typing import List
from app.controllers import controller_selo as ctrl
from app.models.selo_model import ConcederSeloRequest, SeloConcedido, SolicitarSeloRequest
from app.controllers.token import require_permission, get_current_user, TokenPayLoad

router = APIRouter(
    tags=["Selos Concedidos (Instâncias)"],
    responses={404: {"description": "Não encontrado"}},
)


@router.post("/selos/solicitar", status_code=status.HTTP_201_CREATED, summary="Empresa solicita um selo do catálogo", dependencies=[Depends(require_permission("empresa"))])
def solicitar_selo(
    data: SolicitarSeloRequest,
    current_user: TokenPayLoad = Depends(get_current_user)
):
    return ctrl.solicitar_selo_para_minha_empresa(data, current_user)

@router.post("/empresas/{id_empresa}/selos", status_code=status.HTTP_201_CREATED, summary="Concede um selo a uma empresa", dependencies=[Depends(require_permission("admin", "admin_master"))])
def conceder_selo(id_empresa: int, data: ConcederSeloRequest):
    return ctrl.conceder_selo_a_empresa(id_empresa, data)


@router.get("/empresas/{id_empresa}/selos", response_model=List[SeloConcedido], summary="Lista os selos de uma empresa", dependencies=[Depends(require_permission("empresa", "admin", "admin_master"))])
def listar_selos_empresa(id_empresa: int, current_user: TokenPayLoad = Depends(get_current_user)):
    return ctrl.listar_selos_de_empresa(id_empresa, current_user)


@router.get("/selos/solicitacoes", response_model=List[SeloConcedido], summary="Lista todas as solicitações de selo pendentes", dependencies=[Depends(require_permission("admin", "admin_master"))])
def listar_solicitacoes():
    return ctrl.listar_solicitacoes_pendentes()


@router.put("/empresa-selos/{empresa_selo_id}/aprovar", summary="Aprova uma solicitação de selo", dependencies=[Depends(require_permission("admin", "admin_master"))])
def aprovar_selo(empresa_selo_id: int = Path(..., description="O ID da tabela 'empresa_selo'")):
    return ctrl.aprovar_selo_concedido(empresa_selo_id)

@router.put("/empresa-selos/{empresa_selo_id}/recusar", summary="Recusa uma solicitação de selo", dependencies=[Depends(require_permission("admin", "admin_master"))])
def recusar_solicitacao(empresa_selo_id: int = Path(..., description="O ID da tabela 'empresa_selo'")):
    return ctrl.recusar_selo_concedido(empresa_selo_id)

@router.put("/empresa-selos/{empresa_selo_id}/solicitar-renovacao", summary="Solicita a renovação de um selo", dependencies=[Depends(require_permission("empresa"))])
def solicitar_renovacao(
    empresa_selo_id: int = Path(..., description="O ID da tabela 'empresa_selo'"),
    current_user: TokenPayLoad = Depends(get_current_user)
):
    return ctrl.solicitar_renovacao_de_selo(empresa_selo_id, current_user)

@router.delete("/empresa-selos/{empresa_selo_id}", status_code=status.HTTP_200_OK, summary="Revoga um selo concedido", dependencies=[Depends(require_permission("admin", "admin_master"))])
def revogar_selo(empresa_selo_id: int = Path(..., description="O ID da instância do selo a ser revogado")):
    return ctrl.revogar_selo_da_empresa(empresa_selo_id)