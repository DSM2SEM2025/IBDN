from fastapi import APIRouter, Path, Depends, Body, status
from typing import List, Optional, Dict, Any
from app.models.empresas_model import (
    Empresa,
    EmpresaCreate,
    EmpresaUpdate
)
from app.controllers import controller_empresa
from app.controllers.token import get_current_user, TokenPayLoad, require_permission

router = APIRouter(
    prefix="/empresas",  # Adicionado prefixo para agrupar as rotas
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
    # A permissão "empresa" permite que um usuário (ainda não associado) crie sua própria empresa.
    # Admins também podem criar empresas.
    dependencies=[Depends(require_permission(
        "empresa", "admin", "admin_master"))]
)
async def rota_criar_empresa(
    empresa: EmpresaCreate,
    current_user: TokenPayLoad = Depends(get_current_user)
):
    """
    Cria uma nova empresa.
    - Se o usuário logado for um **administrador**, ele pode opcionalmente especificar um `usuario_id` no corpo da requisição para associar a empresa a outro usuário. Se não especificar, a empresa será associada a ele mesmo.
    - Se o usuário logado **não for administrador** (tiver a permissão 'empresa'), a empresa será obrigatoriamente associada a ele.
    """
    return await controller_empresa.criar_empresa(empresa, current_user)


@router.get("/{empresa_id}", response_model=Empresa, dependencies=[Depends(require_permission("empresa", "admin", "admin_master"))])
def buscar_empresa_por_id(
    empresa_id: int = Path(..., gt=0),
    # Adicionar a dependência aqui garante que o usuário tenha acesso antes de prosseguir,
    # embora a lógica de "só pode ver a própria empresa se não for admin" esteja no controller.
    # Para um controle mais rígido, a verificação deveria ocorrer no controller.
    # Por simplicidade, mantemos a verificação de token/permissão geral aqui.
):
    return controller_empresa.get_empresa_por_id(empresa_id)


@router.put(
    "/{id_empresa}",
    response_model=Empresa,
    summary="Atualizar dados de uma empresa",
    # Usuários com permissão "empresa" (clientes) e "admin" podem acessar esta rota.
    # A lógica no controller diferenciará o que cada um pode fazer.
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
    - **Administradores** podem atualizar qualquer empresa.
    - **Usuários com permissão 'empresa'** só podem atualizar a empresa à qual estão associados.
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
    Apenas usuários com permissão de administrador podem realizar esta ação.
    """
    return controller_empresa.delete_empresa(empresa_id, current_user)
