# app/routes/ibdn_permissions_routes.py
from fastapi import APIRouter, HTTPException, status, Query
from typing import List
from app.controllers import ibdn_permissions_controller as ctrl
from app.models.ibdn_user_model import IbdnPermissao, IbdnPermissaoCreate, IbdnPermissaoUpdate

router = APIRouter(
    prefix="/permissoes",
    tags=["IBDN Permissões"],
    responses={404: {"description": "Não encontrado"}},
)


@router.post("/", response_model=IbdnPermissao, status_code=status.HTTP_201_CREATED)
async def api_create_permissao(permissao_data: IbdnPermissaoCreate):
    # Aqui você adicionaria a dependência de autenticação/autorização
    # Ex: current_user: User = Depends(require_permission("gerenciar_permissoes"))
    try:
        return ctrl.create_permissao(permissao_data)
    except HTTPException as e:
        raise e
    except Exception as e:
        # Logar o erro 'e'
        raise HTTPException(
            status_code=500, detail=f"Erro interno do servidor: {str(e)}")


@router.get("/{permissao_id}", response_model=IbdnPermissao)
async def api_get_permissao(permissao_id: str):
    # Adicionar autenticação/autorização se necessário
    try:
        return ctrl.get_permissao(permissao_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro interno do servidor: {str(e)}")


@router.get("/", response_model=List[IbdnPermissao])
async def api_get_all_permissoes(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=1000)):
    # Adicionar autenticação/autorização se necessário
    try:
        return ctrl.get_all_permissoes(skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro interno do servidor: {str(e)}")


@router.put("/{permissao_id}", response_model=IbdnPermissao)
async def api_update_permissao(permissao_id: str, permissao_data: IbdnPermissaoUpdate):
    # Adicionar autenticação/autorização
    try:
        return ctrl.update_permissao(permissao_id, permissao_data)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro interno do servidor: {str(e)}")


@router.delete("/{permissao_id}", status_code=status.HTTP_200_OK)
async def api_delete_permissao(permissao_id: str):
    # Adicionar autenticação/autorização
    try:
        # Retorna uma mensagem de sucesso
        return ctrl.delete_permissao(permissao_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro interno do servidor: {str(e)}")
