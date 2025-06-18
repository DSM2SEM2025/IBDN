from fastapi import APIRouter, Path, Depends, Body, status
from typing import List, Dict, Any
from app.models.empresas_model import (
    Empresa,
    EmpresaCreate,
    EmpresaUpdate
)
from app.controllers import controller_empresa
from app.controllers.token import get_current_user, TokenPayLoad, require_permission

router = APIRouter(
    prefix="/empresas",
    tags=["Empresa"],
    responses={404: {"description": "Não encontrado"}},)


@router.get("/", response_model=List[Empresa], dependencies=[Depends(require_permission("admin", "admin_master"))])
def listar_empresas():
    return controller_empresa.get_empresas()


@router.post(
    "/",
    response_model=Dict[str, Any],
    status_code=status.HTTP_201_CREATED,
    summary="Cria uma nova empresa",
    dependencies=[Depends(require_permission(
        "empresa", "admin", "admin_master"))]
)
def rota_criar_empresa(
    empresa: EmpresaCreate,
    current_user: TokenPayLoad = Depends(get_current_user)
):
    return controller_empresa.criar_empresa(empresa, current_user)


@router.get("/{empresa_id}", response_model=Empresa, dependencies=[Depends(require_permission("empresa", "admin", "admin_master"))])
def buscar_empresa_por_id(
    empresa_id: int = Path(..., gt=0),
    current_user: TokenPayLoad = Depends(get_current_user)
):
    return controller_empresa.get_empresa_por_id(empresa_id, current_user=current_user)


@router.put(
    "/{id_empresa}",
    response_model=Empresa,
    summary="Atualizar dados de uma empresa",
    dependencies=[Depends(require_permission(
        "empresa", "admin", "admin_master"))]
)
def atualizar_empresa_endpoint(
    id_empresa: int = Path(..., gt=0,
                           description="ID da empresa a ser atualizada"),
    empresa_update_data: EmpresaUpdate = Body(...),
    current_user: TokenPayLoad = Depends(get_current_user)
):
    return controller_empresa.update_empresa(
        id_empresa=id_empresa,
        empresa_data=empresa_update_data,
        current_user=current_user
    )


@router.delete(
    "/{empresa_id}",
    status_code=status.HTTP_200_OK,
    summary="Inativar uma empresa (exclusão lógica)",
    dependencies=[Depends(require_permission("admin", "admin_master"))]
)
def excluir_empresa_endpoint(
    empresa_id: int = Path(..., gt=0),
    current_user: TokenPayLoad = Depends(get_current_user)
):
    return controller_empresa.delete_empresa(empresa_id, current_user)