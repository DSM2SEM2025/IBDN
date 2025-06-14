# app/routes/ibdn_profiles_routes.py
from fastapi import APIRouter, HTTPException, status, Query, Depends
from typing import List
from app.controllers import ibdn_profiles_controller as ctrl
from app.models.ibdn_user_model import IbdnPerfil, IbdnPerfilCreate, IbdnPerfilUpdate, PerfilPermissaoLink
from app.controllers.token import require_permission

router = APIRouter(
    prefix="/perfis",
    tags=["IBDN Perfis"],
    responses={404: {"description": "Não encontrado"}},
)


@router.get("/", response_model=List[IbdnPerfil], dependencies=[Depends(require_permission("admin_master", "admin"))])
async def api_get_all_perfis(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=1000)):
    # Adicionar autenticação/autorização
    try:
        return ctrl.get_all_perfis(skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro interno do servidor: {str(e)}")


@router.post("/", response_model=IbdnPerfil, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_permission("admin_master"))])
async def api_create_perfil(perfil_data: IbdnPerfilCreate):
    # Adicionar autenticação/autorização
    try:
        return ctrl.create_perfil(perfil_data)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro interno do servidor: {str(e)}")


@router.get("/{perfil_id}", response_model=IbdnPerfil, dependencies=[Depends(require_permission("admin_master"))])
async def api_get_perfil(perfil_id: str):
    # Adicionar autenticação/autorização
    try:
        return ctrl.get_perfil(perfil_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro interno do servidor: {str(e)}")


@router.put("/{perfil_id}", response_model=IbdnPerfil, dependencies=[Depends(require_permission("admin_master"))])
async def api_update_perfil(perfil_id: str, perfil_update_data: IbdnPerfilUpdate):
    # Adicionar autenticação/autorização
    try:
        return ctrl.update_perfil(perfil_id, perfil_update_data)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro interno do servidor: {str(e)}")


@router.delete("/{perfil_id}", status_code=status.HTTP_200_OK, dependencies=[Depends(require_permission("admin_master"))])
async def api_delete_perfil(perfil_id: str):
    # Adicionar autenticação/autorização
    try:
        return ctrl.delete_perfil(perfil_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro interno do servidor: {str(e)}")


@router.post("/{perfil_id}/permissoes", response_model=IbdnPerfil, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_permission("admin_master"))])
async def api_add_permissao_to_perfil(perfil_id: str, link_data: PerfilPermissaoLink):
    # Adicionar autenticação/autorização
    try:
        return ctrl.add_permissao_to_perfil_ctrl(perfil_id, link_data)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro interno do servidor: {str(e)}")


@router.delete("/{perfil_id}/permissoes/{permissao_id}", response_model=IbdnPerfil, dependencies=[Depends(require_permission("admin_master"))])
async def api_remove_permissao_from_perfil(perfil_id: str, permissao_id: str):
    # Adicionar autenticação/autorização
    try:
        return ctrl.remove_permissao_from_perfil_ctrl(perfil_id, permissao_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro interno do servidor: {str(e)}")
