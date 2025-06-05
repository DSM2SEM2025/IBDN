from fastapi import APIRouter, Path, Depends, Body, status
from typing import List, Optional
from app.models.empresas_model import (
    Empresa, EmpresaCreate, EmpresaDeleteRequest
)
from app.controllers.controller_empresa import (
    get_empresas, criar_empresas, get_empresa_por_id, delete_empresa_by_user
)
from app.controllers.token import get_current_user, TokenPayLoad

router = APIRouter(
    prefix="",
    tags=["Empresa"],
    responses={404: {"description": "Não encontrado"}},)

@router.get("/empresas", response_model=List[Empresa])
def listar_empresas():
    return get_empresas()

@router.post("/empresas")
def adcionar_empresa(empresa: EmpresaCreate):
    return criar_empresas(empresa)

@router.get("/empresas/{empresa_id}", response_model=Empresa)
def buscar_empresa_por_id(empresa_id: int = Path(..., gt=0)):
    return get_empresa_por_id(empresa_id)

@router.delete("/empresa", status_code=status.HTTP_200_OK, summary="Excluir uma empresa")
def excluir_empresa_endpoint(
    delete_request: Optional[EmpresaDeleteRequest] = Body(None),
    current_user: TokenPayLoad = Depends(get_current_user)
):
    """
    Permite a exclusão (lógica) de uma empresa.

    - **Administrador (ADM):** Pode excluir qualquer empresa informando o `empresa_id` no corpo da requisição.
    - **Cliente:** Pode excluir apenas a própria empresa (o `empresa_id` é obtido do token e o corpo da requisição pode ser omitido ou `empresa_id` deve coincidir).
    """
    return delete_empresa_by_user(delete_request, current_user)
