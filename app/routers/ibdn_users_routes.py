# app/routes/ibdn_users_routes.py
from fastapi import APIRouter, HTTPException, status, Query, Depends
from typing import List
from app.controllers import ibdn_users_controller as ctrl
from app.models.ibdn_user_model import IbdnUsuario, IbdnUsuarioCreate, IbdnUsuarioUpdate
from app.controllers.token import require_permission
# Para autenticação/autorização (exemplo, você precisará implementar)
# from app.core.security import get_current_active_user, User # Supondo um schema User para o usuário autenticado
# from app.auth_utils import require_permission # Sua função de dependência para verificar permissões

router = APIRouter(
    prefix="/usuario",
    tags=["IBDN Usuários"],
    responses={404: {"description": "Não encontrado"}},
)


@router.post("/", response_model=IbdnUsuario, status_code=status.HTTP_201_CREATED)
async def api_create_usuario(
    usuario_data: IbdnUsuarioCreate,
    # current_user: User = Depends(require_permission("gerenciar_usuarios")) # Exemplo de proteção
):
    try:
        return ctrl.create_usuario(usuario_data)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro interno do servidor: {str(e)}")


@router.get("/{usuario_id}", response_model=IbdnUsuario, dependencies=[Depends(require_permission("empresa", "admin", "admin_master"))])
async def api_get_usuario(
    usuario_id: str,
    # current_user: User = Depends(get_current_active_user) # Exemplo de proteção
):
    # Aqui você pode adicionar lógica para verificar se o current_user pode ver este usuario_id
    try:
        return ctrl.get_usuario(usuario_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro interno do servidor: {str(e)}")


@router.get("/", response_model=List[IbdnUsuario], dependencies=[Depends(require_permission("admin_master"))])
async def api_get_all_usuarios(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    # current_user: User = Depends(require_permission("listar_usuarios")) # Exemplo de proteção
):
    try:
        return ctrl.get_all_usuarios(skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro interno do servidor: {str(e)}")


@router.put("/{usuario_id}", response_model=IbdnUsuario, dependencies=[Depends(require_permission("admin_master"))])
async def api_update_usuario(
    usuario_id: str,
    usuario_data: IbdnUsuarioUpdate,
    # current_user: User = Depends(get_current_active_user) # Exemplo de proteção
):
    # Adicionar lógica para verificar se current_user pode atualizar este usuario_id
    # ou se tem a permissão "gerenciar_usuarios"
    try:
        return ctrl.update_usuario(usuario_id, usuario_data)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro interno do servidor: {str(e)}")


@router.delete("/{usuario_id}", status_code=status.HTTP_200_OK, dependencies=[Depends(require_permission("admin_master"))])
async def api_delete_usuario(
    usuario_id: str,
    # current_user: User = Depends(require_permission("gerenciar_usuarios")) # Exemplo de proteção
):
    try:
        return ctrl.delete_usuario(usuario_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro interno do servidor: {str(e)}")
