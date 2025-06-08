from fastapi import APIRouter, Path, Depends, Body, status
from typing import List, Optional
from app.models.empresas_model import (
    Empresa, 
    EmpresaCreate, 
    EmpresaDeleteRequest, 
    EmpresaUpdate
)
from app.controllers.controller_empresa import (
    get_empresas, criar_empresas, get_empresa_por_id
)
from app.controllers.token import get_current_user, TokenPayLoad
from app.services import empresa_service
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

@router.delete("/empresas/{empresa_id}", status_code=status.HTTP_200_OK, summary="Excluir uma empresa")
def excluir_empresa_endpoint(
    delete_request: Optional[EmpresaDeleteRequest] = Body(None),
    current_user: TokenPayLoad = Depends(get_current_user)
):
    """Permite a exclusão (lógica) de uma empresa."""
    # A rota agora delega a lógica para a camada de serviço.
    return empresa_service.delete_empresa_service(delete_request, current_user)


@router.put("/empresas/{id_empresa}", response_model=Empresa, summary="Atualizar dados de uma empresa")
def atualizar_empresa_endpoint(
    id_empresa: int = Path(..., gt=0, description="ID da empresa a ser atualizada"),
    empresa_update_data: EmpresaUpdate = Body(...),
    current_user: TokenPayLoad = Depends(get_current_user)
):
    """
    Atualiza os dados de uma empresa existente.

    - **Administrador (ADM):** Pode atualizar qualquer empresa.
    - **Cliente:** Pode atualizar apenas os dados da sua própria empresa.
    """
    return empresa_service.update_empresa_service(
        id_empresa=id_empresa,
        empresa_update_data=empresa_update_data,
        current_user=current_user
    )