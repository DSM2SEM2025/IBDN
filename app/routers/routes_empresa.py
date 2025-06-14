from fastapi import APIRouter, Path, Depends, Body, status
from typing import List, Optional
from app.models.empresas_model import (
    Empresa,
    EmpresaCreate,
    EmpresaDeleteRequest,
    EmpresaUpdate
)
from app.controllers import controller_empresa
from app.controllers.token import get_current_user, TokenPayLoad, require_permission

router = APIRouter(
    prefix="",
    tags=["Empresa"],
    responses={404: {"description": "Não encontrado"}},)


@router.get("/empresas", response_model=List[Empresa], dependencies=[Depends(require_permission("admin"))])
def listar_empresas():
    return controller_empresa.get_empresas()


@router.post(
    "/empresas", 
    status_code=status.HTTP_201_CREATED, 
    summary="Cria uma nova empresa",
    # Protegemos a rota. Quem pode criar empresas? Ex: todos os usuários logados.
    dependencies=[Depends(require_permission("empresa", "admin", "admin_master"))]
)
async def rota_criar_empresa(
    empresa: EmpresaCreate,
    current_user: TokenPayLoad = Depends(get_current_user)
):
    """
    Cria uma nova empresa. A empresa será associada ao usuário logado,
    a menos que o usuário seja um admin e especifique outro usuário.
    """
    return await controller_empresa.criar_empresa(empresa, current_user)


@router.get("/empresas/{empresa_id}", response_model=Empresa, dependencies=[Depends(require_permission("empresa", "admin"))])
def buscar_empresa_por_id(empresa_id: int = Path(..., gt=0)):
    return controller_empresa.get_empresa_por_id(empresa_id)


@router.delete("/empresas/{empresa_id}", status_code=status.HTTP_200_OK, summary="Excluir uma empresa", dependencies=[Depends(require_permission("admin"))])
def excluir_empresa_endpoint(
    delete_request: Optional[EmpresaDeleteRequest] = Body(None),
    current_user: TokenPayLoad = Depends(get_current_user)
):
    """Permite a exclusão (lógica) de uma empresa."""
    # Chama diretamente a nova função completa do controller
    return controller_empresa.delete_empresa(delete_request, current_user)


@router.put("/empresas/{id_empresa}", response_model=Empresa, summary="Atualizar dados de uma empresa", dependencies=[Depends(require_permission("empresa","admin"))])
def atualizar_empresa_endpoint(
    id_empresa: int = Path(..., gt=0,
                           description="ID da empresa a ser atualizada"),
    empresa_update_data: EmpresaUpdate = Body(...),
    current_user: TokenPayLoad = Depends(get_current_user)
):
    """Atualiza os dados de uma empresa existente."""
    # Chama diretamente a nova função completa do controller
    return controller_empresa.update_empresa(
        id_empresa=id_empresa,
        empresa_data=empresa_update_data,
        current_user=current_user
    )
