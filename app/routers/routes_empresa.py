# teste_1/back/app/routers/routes_empresa.py

from fastapi import APIRouter, Path, Depends, Body, status
from typing import List, Dict, Any
from app.models.empresas_model import (
    Empresa,
    EmpresaCreate,
    EmpresaUpdate
)
from app.controllers import controller_empresa
# MODIFICAÇÃO: get_current_user também será usado na rota de busca por ID
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
    """
    Cria uma nova empresa.
    """
    return controller_empresa.criar_empresa(empresa, current_user)

# MODIFICAÇÃO: A rota agora depende de get_current_user e o passa para o controller


@router.get("/{empresa_id}", response_model=Empresa, dependencies=[Depends(require_permission("empresa", "admin", "admin_master"))])
def buscar_empresa_por_id(
    empresa_id: int = Path(..., gt=0),
    current_user: TokenPayLoad = Depends(get_current_user)  # Adicionado
):
    # Adicionado
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
    """
    Atualiza os dados de uma empresa existente.
    """
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
    """
    Permite a exclusão (lógica) de uma empresa.
    """
    return controller_empresa.delete_empresa(empresa_id, current_user)
