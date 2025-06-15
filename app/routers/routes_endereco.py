from fastapi import APIRouter, Path, Depends
from typing import List
from app.controllers.controller_endereco import get_empresa_enderecos_by_empresa_id, update_empresa_endereco, create_empresa_endereco,  delete_empresa_endereco
from app.models.model_endereco import EmpresaEndereco, EmpresaEnderecoUpdate, EmpresaEnderecoCreate
from app.controllers.token import require_permission, TokenPayLoad, get_current_user

router = APIRouter(
    prefix="",
    tags=["Endereco"],
    responses={404: {"description": "Não encontrado"}},
)

@router.get("/empresas/{empresa_id}/enderecos", response_model=List[EmpresaEndereco], dependencies=[Depends(require_permission("empresa", "admin", "admin_master"))])
def listar_enderecos_da_empresa(
    empresa_id: int = Path(..., gt=0),
    current_user: TokenPayLoad = Depends(get_current_user)
):
    """
    Lista os endereços de uma empresa.
    - Administradores podem ver qualquer um.
    - Usuários 'empresa' só podem ver o seu próprio.
    """
    return get_empresa_enderecos_by_empresa_id(empresa_id, current_user)

@router.post("/empresas/{empresa_id}/endereco", status_code=201, dependencies=[Depends(require_permission("empresa", "admin", "admin_master"))])
def criar_novo_endereco(
    data: EmpresaEnderecoCreate,
    empresa_id: int = Path(..., gt=0),
    current_user: TokenPayLoad = Depends(get_current_user) # <- Pega os dados do token
):
    return create_empresa_endereco(empresa_id, data, current_user)

@router.put("/empresas/{empresa_id}/endereco", dependencies=[Depends(require_permission("empresa", "admin"))])
def atualizar_endereco_da_empresa(
    data: EmpresaEnderecoUpdate,
    empresa_id: int = Path(..., gt=0),
    current_user: TokenPayLoad = Depends(get_current_user)  # <- Essencial injetar o usuário
):
    # A função do controller agora recebe o current_user
    return update_empresa_endereco(empresa_id, data, current_user)

@router.delete("/empresas/{empresa_id}/endereco", status_code=200, dependencies=[Depends(require_permission("admin", "admin_master"))])
def remover_endereco_da_empresa(empresa_id: int = Path(..., gt=0)):
    return delete_empresa_endereco(empresa_id)