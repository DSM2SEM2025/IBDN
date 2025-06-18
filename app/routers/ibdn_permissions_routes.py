from fastapi import APIRouter, HTTPException, status, Query, Depends
from typing import List
from app.controllers import ibdn_permissions_controller as ctrl
from app.models.ibdn_user_model import IbdnPermissao, IbdnPermissaoCreate, IbdnPermissaoUpdate
from app.controllers.token import require_permission

router = APIRouter(
    prefix="/permissoes",
    tags=["IBDN Permissões"],
    responses={404: {"description": "Não encontrado"}},
)


@router.post("/", response_model=IbdnPermissao, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_permission("admin_master"))])
async def api_create_permissao(permissao_data: IbdnPermissaoCreate):
    try:
        return ctrl.create_permissao(permissao_data)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro interno do servidor: {str(e)}")


@router.get("/{permissao_id}", response_model=IbdnPermissao, dependencies=[Depends(require_permission("admin_master"))])
async def api_get_permissao(permissao_id: str):
    try:
        return ctrl.get_permissao(permissao_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro interno do servidor: {str(e)}")


@router.get("/", response_model=List[IbdnPermissao], dependencies=[Depends(require_permission("admin_master"))])
async def api_get_all_permissoes(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=1000)):
    try:
        return ctrl.get_all_permissoes(skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro interno do servidor: {str(e)}")


@router.put("/{permissao_id}", response_model=IbdnPermissao, dependencies=[Depends(require_permission("admin_master"))])
async def api_update_permissao(permissao_id: str, permissao_data: IbdnPermissaoUpdate):
    try:
        return ctrl.update_permissao(permissao_id, permissao_data)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro interno do servidor: {str(e)}")


@router.delete("/{permissao_id}", status_code=status.HTTP_200_OK, dependencies=[Depends(require_permission("admin_master"))])
async def api_delete_permissao(permissao_id: str):
    try:
        return ctrl.delete_permissao(permissao_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro interno do servidor: {str(e)}")