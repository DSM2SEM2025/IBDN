from fastapi import APIRouter, HTTPException, status, Query, Depends
from typing import List
from app.controllers import ibdn_users_controller as ctrl
from app.models.ibdn_user_model import IbdnUsuario, IbdnUsuarioCreate, IbdnUsuarioUpdate, UsuarioRegister
from app.controllers.token import require_permission, get_current_user, TokenPayLoad

router = APIRouter(
    prefix="/usuario",
    tags=["IBDN Usuários"],
    responses={404: {"description": "Não encontrado"}},
)

@router.post("/register", response_model=IbdnUsuario, status_code=status.HTTP_201_CREATED, summary="Autocadastro de um novo usuário")
async def api_register_user(usuario_data: UsuarioRegister):
    try:
        return ctrl.register_new_user(usuario_data)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno do servidor: {str(e)}"
        )
    
@router.post("/", response_model=IbdnUsuario, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_permission("admin", "admin_master"))])
async def api_create_usuario(
    usuario_data: IbdnUsuarioCreate,
):
    try:
        return ctrl.create_usuario(usuario_data)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro interno do servidor: {str(e)}")


@router.get("/{usuario_id}", response_model=IbdnUsuario)
async def api_get_usuario(
    usuario_id: str,
    current_user: TokenPayLoad = Depends(get_current_user)
):
    try:
        return ctrl.get_usuario(usuario_id, current_user)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro interno do servidor: {str(e)}")


@router.get("/", response_model=List[IbdnUsuario], dependencies=[Depends(require_permission("admin_master"))])
async def api_get_all_usuarios(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
):
    try:
        return ctrl.get_all_usuarios(skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro interno do servidor: {str(e)}")


@router.put("/{usuario_id}", response_model=IbdnUsuario, dependencies=[Depends(require_permission("empresa", "admin", "admin_master"))])
async def api_update_usuario(
    usuario_id: str,
    usuario_data: IbdnUsuarioUpdate,
    current_user: TokenPayLoad = Depends(get_current_user)
):
    try:
        return ctrl.update_usuario(usuario_id, usuario_data, current_user)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro interno do servidor: {str(e)}")


@router.delete("/{usuario_id}", status_code=status.HTTP_200_OK, dependencies=[Depends(require_permission("admin", "admin_master"))])
async def api_delete_usuario(
    usuario_id: str,
):
    try:
        return ctrl.delete_usuario(usuario_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro interno do servidor: {str(e)}")